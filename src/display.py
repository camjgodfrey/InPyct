from rich.console import Console
from rich.tree import Tree
from typing import Dict, Any, Optional
from models import CodeAnalysis
from helper import display_message, format_ai_insights
from constants import (
    PROJECT_STATISTICS_TEMPLATE,
    ANALYSIS_RESULTS_PANEL_TITLE,
    ANALYSIS_RESULTS_BORDER,
    AI_INSIGHTS_TITLE,
    AI_INSIGHTS_PANEL_BORDER,
    NO_AI_INSIGHTS_MESSAGE,
)


class DisplayManager:
    def __init__(self):
        self.console = Console()

    def display_tree(self, analysis: Optional[CodeAnalysis] = None) -> None:
        """Displays the file tree and analysis results using Rich."""
        if not analysis:
            return

        # Add spacing for better separation
        self.console.print()
        
        # Display tree with enhanced styling
        tree = Tree("[bold blue]📁 Project Root[/bold blue]")
        self._build_tree_view(analysis.file_tree, tree)
        self.console.print(tree)
        
        # Add separator
        self.console.print("\n[dim]" + "─" * 80 + "[/dim]\n")
        
        self._display_statistics(analysis)
        
        # Add separator
        self.console.print("\n[dim]" + "─" * 80 + "[/dim]\n")
        
        self._display_insights(analysis)

    def _display_statistics(self, analysis: CodeAnalysis) -> None:
        """Displays project statistics."""
        stats_text = PROJECT_STATISTICS_TEMPLATE.format(
            total_dirs=analysis.total_dirs,
            total_files=analysis.total_files,
            total_python_files=len(analysis.python_files),
        )
        display_message(
            self.console,
            stats_text,
            ANALYSIS_RESULTS_PANEL_TITLE,
            ANALYSIS_RESULTS_BORDER,
        )

    def _display_insights(self, analysis: CodeAnalysis) -> None:
        """Displays AI insights with enhanced formatting."""
        if analysis.ai_insights:
            insights_text = format_ai_insights(analysis.ai_insights)
            # Use a panel with a distinctive style
            display_message(
                self.console,
                insights_text,
                AI_INSIGHTS_TITLE,
                AI_INSIGHTS_PANEL_BORDER,
                padding=(1, 2)  # Add padding for better readability
            )
        else:
            display_message(
                self.console,
                "[yellow]No AI insights available for this project.[/yellow]",
                border_style="yellow"
            )

    def _build_tree_view(self, file_tree: Dict[str, Any], tree: Tree) -> None:
        """Recursively builds the Rich tree view for displaying file structure."""
        for name, subtree in sorted(file_tree.items()):
            if isinstance(subtree, dict):  # Check if it's a directory
                branch = tree.add(f"[bold green]{name}")
                self._build_tree_view(subtree, branch)
            else:  # It's a file
                tree.add(f"[bold cyan]{name}")
