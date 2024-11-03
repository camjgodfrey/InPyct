import aiohttp
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from models import FileInsights
from constants import (
    WELCOME_MESSAGE,
    GOODBYE_MESSAGE,
    ERROR_DURING_ANALYSIS_MESSAGE,
    NO_AI_INSIGHTS_MESSAGE,
    ERROR_API_RESPONSE,
    OLLAMA_API_URL,
    FILE_HEADER_TEMPLATE,
    ANALYSIS_SECTION_HEADER,
    RECOMMENDATIONS_SECTION_HEADER,
)


def display_message(
    console: Console,
    message: str,
    title: Optional[str] = None,
    border_style: str = "blue",
    padding: Tuple[int, int] = (0, 1)
) -> None:
    """Displays a message in a Rich Panel with customizable padding."""
    panel = Panel(
        message,
        title=title,
        border_style=border_style,
        padding=padding
    )
    console.print(panel)


def display_welcome(console: Console) -> None:
    """Displays the welcome message."""
    display_message(console, WELCOME_MESSAGE, title="Python Project Analyzer")


def display_goodbye(console: Console) -> None:
    """Displays the goodbye message."""
    console.print(GOODBYE_MESSAGE)


async def prompt_directory(console: Console) -> Optional[Path]:
    """Prompts the user to enter a valid directory path or exit."""
    dir_path = Prompt.ask(
        "\n[cyan]Enter the directory path to analyze or type 'exit' to quit:[/cyan]"
    )
    if dir_path.lower() in ("exit", "quit", "q"):
        return None

    directory = Path(dir_path).resolve()
    if not directory.is_dir():
        console.print(f"[red]Invalid directory: {directory}[/red]")
        return await prompt_directory(console)  

    return directory


def handle_analysis_error(console: Console, error: Exception) -> None:
    """Displays an error message encountered during analysis."""
    console.print(ERROR_DURING_ANALYSIS_MESSAGE.format(error=error))


def format_ai_insights(ai_insights: Dict[str, FileInsights]) -> str:
    """Formats the AI insights with enhanced styling."""
    if not ai_insights:
        return NO_AI_INSIGHTS_MESSAGE

    sections = []
    for file, insights in ai_insights.items():
        # Create a section for each file
        section = []
        section.append(FILE_HEADER_TEMPLATE.format(filename=file))
        
        # Add analysis with header
        section.append(ANALYSIS_SECTION_HEADER)
        section.append(insights.analysis)
        
        # Add recommendations with header
        section.append(RECOMMENDATIONS_SECTION_HEADER)
        # Split recommendations into bullet points if they contain newlines
        recommendations = insights.recommendations.split('\n')
        formatted_recommendations = [
            f"[yellow]•[/yellow] {rec.strip()}" 
            for rec in recommendations 
            if rec.strip()
        ]
        section.append('\n'.join(formatted_recommendations))
        
        sections.append('\n'.join(section))
    
    return '\n\n'.join(sections)


async def send_ollama_request(
    console: Console,
    session: aiohttp.ClientSession,
    payload: Dict[str, Any],
    file_name: str,
    request_type: str,
) -> str:
    """Sends a request to the Ollama API and handles errors."""
    try:
        async with session.post(OLLAMA_API_URL, json=payload) as response:
            if response.status == 200:
                resp_json = await response.json()
                return resp_json.get("response", "").strip()
            console.print(
                ERROR_API_RESPONSE.format(
                    request_type=request_type,
                    file_name=file_name,
                    status=response.status,
                )
            )
    except Exception as e:
        console.print(f"[red]API request failed: {str(e)}[/red]")
    return ""


def format_prompt(template: str, **kwargs) -> str:
    """Formats a prompt template with the specified parameters."""
    return template.format(**kwargs)


def read_python_file(file_path: Path) -> str:
    """Reads a Python file with UTF-8 encoding and handles read errors."""
    try:
        return file_path.read_text(encoding="utf-8")
    except Exception as e:
        raise ValueError(f"Failed to read file {file_path}: {str(e)}")
