import aiohttp
from typing import Dict, List
from pathlib import Path
from models import FileInsights
from rich.console import Console
from constants import (
    OLLAMA_MODEL_ANALYSIS,
    OLLAMA_MODEL_SUMMARIZE,
    ANALYSIS_PROMPT_TEMPLATE,
    RECOMMENDATIONS_PROMPT_TEMPLATE,
    SUMMARIZE_PROMPT_TEMPLATE,
    ERROR_ANALYZING_FILE,
    DEFAULT_ANALYSIS,
    DEFAULT_RECOMMENDATIONS,
)
from helper import send_ollama_request, format_prompt, read_python_file


class AIIntegration:
    def __init__(self):
        self.console = Console()

    async def get_ai_insights(
        self, python_files: List[Path]
    ) -> Dict[str, FileInsights]:
        """Gets AI analysis and recommendations for each Python file using Ollama."""
        insights = {}
        async with aiohttp.ClientSession() as session:
            for file_path in python_files:
                insights[file_path.name] = await self._analyze_file(session, file_path)
        return insights

    async def _analyze_file(
        self, session: aiohttp.ClientSession, file_path: Path
    ) -> FileInsights:
        """Performs AI analysis and recommendation generation for a single file."""
        try:
            code = read_python_file(file_path)
            analysis = await self._get_analysis(session, file_path, code)
            recommendations = await self._get_recommendations(
                session, file_path, analysis
            )
            summarized_recommendations = await self._summarize_recommendations(
                session, file_path, recommendations
            )

            return FileInsights(
                analysis=analysis or DEFAULT_ANALYSIS,
                recommendations=summarized_recommendations or DEFAULT_RECOMMENDATIONS,
            )
        except Exception as e:
            self._report_error(file_path, e)
            return FileInsights()

    async def _get_analysis(
        self, session: aiohttp.ClientSession, file_path: Path, code: str
    ) -> str:
        """Fetches the analysis for the given code using Ollama."""
        prompt = format_prompt(
            ANALYSIS_PROMPT_TEMPLATE, file_name=file_path.name, code=code
        )
        return await self._send_request(
            session, prompt, file_path, "analysis", OLLAMA_MODEL_ANALYSIS
        )

    async def _get_recommendations(
        self, session: aiohttp.ClientSession, file_path: Path, analysis: str
    ) -> str:
        """Fetches recommendations based on the analysis."""
        prompt = format_prompt(RECOMMENDATIONS_PROMPT_TEMPLATE, analysis=analysis)
        return await self._send_request(
            session, prompt, file_path, "recommendations", OLLAMA_MODEL_ANALYSIS
        )

    async def _summarize_recommendations(
        self, session: aiohttp.ClientSession, file_path: Path, recommendations: str
    ) -> str:
        """Summarizes the recommendations for concise output."""
        prompt = format_prompt(
            SUMMARIZE_PROMPT_TEMPLATE, recommendations=recommendations
        )
        return await self._send_request(
            session, prompt, file_path, "summarize", OLLAMA_MODEL_SUMMARIZE
        )

    async def _send_request(
        self,
        session: aiohttp.ClientSession,
        prompt: str,
        file_path: Path,
        task_type: str,
        model: str,
    ) -> str:
        """Sends a request to the Ollama model with the specified prompt."""
        return await send_ollama_request(
            self.console,
            session,
            {
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
            file_path.name,
            task_type,
        )

    def _report_error(self, file_path: Path, error: Exception) -> None:
        """Reports an error during file analysis."""
        self.console.print(
            ERROR_ANALYZING_FILE.format(file_name=file_path.name, error=str(error))
        )
