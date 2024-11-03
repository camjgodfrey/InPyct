import aiohttp
import re
from typing import Dict, List
from pathlib import Path
from models import FileInsights, RankedRecommendation
from rich.console import Console
from constants import (
    OLLAMA_MODEL_ANALYSIS,
    OLLAMA_MODEL_SUMMARIZE,
    ANALYSIS_PROMPT_TEMPLATE,
    RECOMMENDATIONS_PROMPT_TEMPLATE,
    SUMMARIZE_PROMPT_TEMPLATE,
    ERROR_ANALYZING_FILE,
    DEFAULT_RECOMMENDATIONS,
    RANKING_PROMPT_TEMPLATE,
    OLLAMA_MODEL_RANKING,
)
from helper import send_ollama_request, format_prompt, read_python_file


class AIIntegration:
    def __init__(self):
        self.console = Console()

    def _clean_response(self, response: str) -> str:
        """Cleans response text by removing code blocks and other unwanted elements."""
        if not response:
            return ""

        # Use raw strings for regex patterns
        # Remove code blocks with language specification
        response = re.sub(r"```[a-zA-Z0-9]*[\r\n].*?```", "", response, flags=re.DOTALL)
        # Remove any remaining code blocks
        response = re.sub(r"```.*?```", "", response, flags=re.DOTALL)
        # Remove inline code
        response = re.sub(r"`.*?`", "", response)
        # Remove any HTML-like tags
        response = re.sub(r"<[^>]+>", "", response)
        # Remove multiple newlines and extra spaces
        response = re.sub(r"\n\s*\n", "\n\n", response)
        response = re.sub(r" +", " ", response)
        # Remove leading/trailing whitespace
        response = response.strip()

        return response

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
        """Fetches and cleans recommendations based on the analysis."""
        enhanced_prompt = (
            "IMPORTANT: DO NOT INCLUDE ANY CODE EXAMPLES OR SNIPPETS IN YOUR RESPONSE.\n\n"
            + format_prompt(RECOMMENDATIONS_PROMPT_TEMPLATE, analysis=analysis)
        )

        response = await self._send_request(
            session,
            enhanced_prompt,
            file_path,
            "recommendations",
            OLLAMA_MODEL_ANALYSIS,
        )

        cleaned_response = self._clean_response(response)

        # Format checker and fixer
        if not all(
            marker in cleaned_response
            for marker in ["RECOMMENDATION:", "RATIONALE:", "OUTCOME:"]
        ):
            self.console.print(
                f"[yellow]Warning: Reformatting recommendations for {file_path.name}[/yellow]"
            )

            # Attempt to structure the response if it contains useful information
            if cleaned_response:
                lines = cleaned_response.split("\n")
                structured_response = []

                for line in lines:
                    if line.strip():
                        structured_response.extend(
                            [
                                "RECOMMENDATION: " + line,
                                "RATIONALE: Identified during code analysis",
                                "OUTCOME: Improved code quality\n",
                            ]
                        )

                return "\n".join(structured_response)

            return DEFAULT_RECOMMENDATIONS

        return cleaned_response

    async def _rank_recommendations(
        self,
        session: aiohttp.ClientSession,
        file_path: Path,
        analysis: str,
        recommendations: str,
    ) -> List[RankedRecommendation]:
        """Ranks recommendations based on impact and relevance."""
        try:
            enhanced_prompt = (
                "IMPORTANT: DO NOT INCLUDE ANY CODE EXAMPLES OR SNIPPETS IN YOUR RESPONSE.\n\n"
                + format_prompt(
                    RANKING_PROMPT_TEMPLATE,
                    analysis=analysis,
                    recommendations=recommendations,
                )
            )

            response = await self._send_request(
                session, enhanced_prompt, file_path, "ranking", OLLAMA_MODEL_RANKING
            )

            cleaned_response = self._clean_response(response)

            if not cleaned_response:
                return []

            ranked_recommendations = []
            current_priority = None

            # Process line by line
            lines = [
                line.strip() for line in cleaned_response.split("\n") if line.strip()
            ]

            for i, line in enumerate(lines):
                if line.startswith("### "):
                    current_priority = line.replace("### ", "").strip()
                    continue

                if (
                    line.startswith("[")
                    and "(Impact:" in line
                    and current_priority is not None
                ):

                    try:
                        impact_match = re.search(r"Impact:\s*(\d+)/5", line)
                        if not impact_match:
                            continue

                        impact = int(impact_match.group(1))
                        if impact < 3:
                            continue

                        text_match = re.search(r"\)\s*(.*?)$", line)
                        if not text_match:
                            continue

                        text = text_match.group(1).strip()

                        justification = "No justification provided"
                        if i + 1 < len(lines):
                            next_line = lines[i + 1].strip()
                            if next_line.startswith("- Justification:"):
                                justification = next_line[
                                    len("- Justification:") :
                                ].strip()

                        ranked_recommendations.append(
                            RankedRecommendation(
                                text=text,
                                priority=current_priority,
                                impact_score=impact,
                                justification=justification,
                            )
                        )

                    except ValueError as e:
                        self.console.print(
                            f"[yellow]Failed to parse recommendation: {str(e)}[/yellow]"
                        )

            # Sort recommendations
            priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
            return sorted(
                ranked_recommendations,
                key=lambda x: (priority_order.get(x.priority, 999), -x.impact_score),
            )

        except Exception as e:
            self.console.print(f"[red]Error in _rank_recommendations: {str(e)}[/red]")
            return []

    async def _summarize_recommendations(
        self, session: aiohttp.ClientSession, file_path: Path, recommendations: str
    ) -> str:
        """Summarizes and cleans the recommendations for concise output."""
        enhanced_prompt = (
            "IMPORTANT: DO NOT INCLUDE ANY CODE EXAMPLES OR SNIPPETS IN YOUR RESPONSE.\n\n"
            + format_prompt(SUMMARIZE_PROMPT_TEMPLATE, recommendations=recommendations)
        )

        response = await self._send_request(
            session, enhanced_prompt, file_path, "summarize", OLLAMA_MODEL_SUMMARIZE
        )

        cleaned_response = self._clean_response(response)

        # Format checker and fixer
        if not re.search(r"SUMMARY #\d+:", cleaned_response):
            self.console.print(
                f"[yellow]Warning: Reformatting summary for {file_path.name}[/yellow]"
            )

            # Attempt to structure the response if it contains useful information
            if cleaned_response:
                lines = cleaned_response.split("\n")
                structured_response = []

                for i, line in enumerate(lines, 1):
                    if line.strip():
                        structured_response.append(f"SUMMARY #{i}: {line.strip()}\n")

                return "\n".join(structured_response)

            return recommendations

        return cleaned_response

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
