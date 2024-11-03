# main.py

WELCOME_MESSAGE = (
    "[yellow]Welcome to the Python Project Analyzer![/yellow]\n\n"
    "This tool analyzes your Python project structure and generates recommendations using AI."
)

GOODBYE_MESSAGE = "[yellow]Goodbye![/yellow]"
NO_PYTHON_FILES_MESSAGE = "[red]No Python files found in the specified directory.[/red]"
INVALID_DIRECTORY_MESSAGE = "[red]Invalid directory: {directory}[/red]"
ERROR_DURING_ANALYSIS_MESSAGE = "[bold red]Error during analysis: {error}[/bold red]"
PROMPT_MESSAGE = (
    "\n[cyan]Enter the directory path to analyze or type 'exit' to quit:[/cyan]"
)

ANALYSIS_START_MESSAGE = "[bold yellow]Starting analysis of: {directory}[/bold yellow]"

ANALYSIS_COMPLETE_TEMPLATE = """
[bold green]Analysis complete:[/bold green]
• Directories found: {total_dirs}
• Files found: {total_files}
• Python files found: {total_python_files}
"""

PROGRESS_SPINNER_TEXT = "[cyan]Generating AI analysis and recommendations...[/cyan]"

# models.py

DEFAULT_ANALYSIS = "No analysis available."
DEFAULT_RECOMMENDATIONS = "No recommendations available."

# display.py

PROJECT_STATISTICS_TEMPLATE = """
[bold green]Project Statistics:[/bold green]
• Total directories: {total_dirs}
• Total files: {total_files}
• Python files: {total_python_files}
"""

AI_INSIGHTS_TITLE = "AI Insights and Recommendations"

NO_AI_INSIGHTS_MESSAGE = "No AI insights available."

WELCOME_PANEL_TITLE = "Python Project Analyzer"
WELCOME_PANEL_BORDER = "blue"

ANALYSIS_RESULTS_PANEL_TITLE = "Analysis Results"
ANALYSIS_RESULTS_BORDER = "green"

AI_INSIGHTS_PANEL_BORDER = "cyan"

# api_integration.py

OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL_ANALYSIS = "gemma2:9b-instruct-q5_0"
OLLAMA_MODEL_SUMMARIZE = "llama3.2:3b-instruct-q5_0"

ANALYSIS_PROMPT_TEMPLATE = """Provide a comprehensive analysis of the following Python code. Focus on its functionality, structure, and the relationships between modules, classes, and methods.

**File:** {file_name}

{code}
"""

RECOMMENDATIONS_PROMPT_TEMPLATE = """Based on the following analysis, provide detailed, specific, and actionable recommendations to improve the Python code.

**Analysis:**
{analysis}
"""

SUMMARIZE_PROMPT_TEMPLATE = """For each of the following recommendations, create a comprehensive paragraph that ensures the recommendation is specific, measurable, achievable, realistic, and timely (SMART). Do not mention the SMART criteria explicitly.

{recommendations}
"""

ERROR_ANALYZING_FILE = "[red]Error analyzing {file_name}: {error}[/red]"
ERROR_API_RESPONSE = "[red]Failed to get response for {request_type} of {file_name}. HTTP Status: {status}[/red]"
