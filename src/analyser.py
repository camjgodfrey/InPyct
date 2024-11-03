from pathlib import Path
from typing import Any, Dict, List, Tuple
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import aiohttp
from models import CodeAnalysis, FileInsights
from helper import display_message, read_python_file
from constants import (
    ANALYSIS_START_MESSAGE,
    ANALYSIS_COMPLETE_TEMPLATE,
    PROGRESS_FILE_TEXT,
    ANALYSIS_STAGES,
    PROGRESS_STATUS_TEXT,
    STAGE_ANALYSIS,
    STAGE_RECOMMENDATIONS,
    STAGE_RANKING,
    STAGE_SUMMARY,
)
from api_integration import AIIntegration


class CodeAnalyzer:
    def __init__(self):
        self.console = Console()
        self.ai_integration = AIIntegration()

    async def analyze_directory(self, directory: Path) -> CodeAnalysis:
        if not directory.exists():
            raise ValueError(f"Directory does not exist: {directory}")
        if not directory.is_dir():
            raise ValueError(f"Path is not a directory: {directory}")

        display_message(
            self.console, ANALYSIS_START_MESSAGE.format(directory=directory)
        )

        python_files, total_files, total_dirs = self._collect_directory_stats(directory)
        file_tree = self._build_file_tree(directory)

        stats_message = ANALYSIS_COMPLETE_TEMPLATE.format(
            total_dirs=total_dirs,
            total_files=total_files,
            total_python_files=len(python_files),
        )
        display_message(self.console, stats_message, border_style="green")

        ai_insights = (
            await self._generate_ai_insights(python_files) if python_files else {}
        )

        return CodeAnalysis(
            file_tree=file_tree,
            python_files=python_files,
            total_files=total_files,
            total_dirs=total_dirs,
            ai_insights=ai_insights,
        )

    def _collect_directory_stats(self, directory: Path) -> Tuple[List[Path], int, int]:
        """Collects statistics for files and directories, focusing on Python files."""
        total_files = 0
        total_dirs = 0
        python_files = []

        for path in directory.rglob("*"):
            if self._is_ignored(path, directory):
                continue
            if path.is_file():
                total_files += 1
                if path.suffix == ".py":
                    python_files.append(path)
            elif path.is_dir():
                total_dirs += 1

        return python_files, total_files, total_dirs

    def _is_ignored(self, path: Path, root: Path) -> bool:
        """Determines if a path should be ignored (hidden files, __pycache__)."""
        return (
            any(part.startswith(".") for part in path.relative_to(root).parts)
            or path.name == "__pycache__"
        )

    def _build_file_tree(self, directory: Path) -> Dict[str, Any]:
        """Recursively builds a dictionary representation of the file tree."""
        return {
            item.name: self._build_file_tree(item) if item.is_dir() else None
            for item in directory.iterdir()
            if not self._is_ignored(item, directory)
        }

    async def _generate_ai_insights(self, python_files: List[Path]) -> Dict[str, Any]:
        """Generates AI insights for each Python file with a progress spinner."""
        async with aiohttp.ClientSession() as session:
            return await self._fetch_ai_insights_with_progress(session, python_files)

    async def _fetch_ai_insights_with_progress(
        self, session: aiohttp.ClientSession, python_files: List[Path]
    ) -> Dict[str, Any]:
        if not python_files:
            return {}
        insights = {}
        total_files = len(python_files)

        progress_columns = [
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TextColumn("•"),
            TextColumn(
                "[progress.description]{task.fields[stage]}"
            ),  
        ]

        with Progress(*progress_columns, console=self.console) as progress:
            main_task = progress.add_task(
                "",
                total=total_files,
                stage=ANALYSIS_STAGES[STAGE_ANALYSIS],  
            )

            for idx, file_path in enumerate(python_files, 1):
                try:
                    progress.update(
                        main_task,
                        description=PROGRESS_FILE_TEXT.format(
                            current_file=file_path.name, current=idx, total=total_files
                        ),
                        stage=ANALYSIS_STAGES[STAGE_ANALYSIS],
                    )

                    # Analysis stage
                    progress.update(main_task, stage=ANALYSIS_STAGES[STAGE_ANALYSIS])
                    analysis = await self.ai_integration._get_analysis(
                        session, file_path, read_python_file(file_path)
                    )

                    # Recommendations stage
                    progress.update(
                        main_task, stage=ANALYSIS_STAGES[STAGE_RECOMMENDATIONS]
                    )
                    recommendations = await self.ai_integration._get_recommendations(
                        session, file_path, analysis
                    )

                    # Ranking stage
                    progress.update(main_task, stage=ANALYSIS_STAGES[STAGE_RANKING])
                    ranked_recs = await self.ai_integration._rank_recommendations(
                        session, file_path, analysis, recommendations
                    )

                    # Summary stage
                    progress.update(main_task, stage=ANALYSIS_STAGES[STAGE_SUMMARY])
                    summary = await self.ai_integration._summarize_recommendations(
                        session,
                        file_path,
                        "\n".join(f"{r.text} - {r.justification}" for r in ranked_recs),
                    )

                    insights[file_path.name] = FileInsights(
                        analysis=analysis,
                        ranked_recommendations=ranked_recs,
                        recommendations=summary,
                    )

                    self.console.print(
                        PROGRESS_STATUS_TEXT.format(
                            filename=file_path.name, status="✓ Analysis complete"
                        )
                    )
                    progress.advance(main_task)

                except Exception as e:
                    self.console.print(
                        f"[red]Error analyzing {file_path.name}: {str(e)}[/red]"
                    )
                    progress.advance(main_task)

        return insights
