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


DEFAULT_ANALYSIS = "No analysis available."
DEFAULT_RECOMMENDATIONS = "No recommendations available."


PROJECT_STATISTICS_TEMPLATE = """
[bold cyan]Project Statistics[/bold cyan]
[green]• Directories:[/green] {total_dirs}
[green]• Total Files:[/green] {total_files} 
[green]• Python Files:[/green] {total_python_files}
"""

FILE_HEADER_TEMPLATE = "\n[bold magenta]━━━ {filename} ━━━[/bold magenta]\n"

ANALYSIS_SECTION_HEADER = "\n[bold blue]Analysis[/bold blue]\n"
RECOMMENDATIONS_SECTION_HEADER = "\n[bold green]Recommendations[/bold green]\n"

AI_INSIGHTS_TITLE = "AI Insights and Recommendations"

NO_AI_INSIGHTS_MESSAGE = "No AI insights available."

WELCOME_PANEL_TITLE = "Python Project Analyzer"
WELCOME_PANEL_BORDER = "blue"

ANALYSIS_RESULTS_PANEL_TITLE = "[bold cyan]Analysis Results[/bold cyan]"
ANALYSIS_RESULTS_BORDER = "cyan"
AI_INSIGHTS_PANEL_BORDER = "magenta"

OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL_ANALYSIS = "gemma2:9b-instruct-q5_0"
OLLAMA_MODEL_SUMMARIZE = "llama3.2:3b-instruct-q5_0"

ANALYSIS_PROMPT_TEMPLATE = """
Analyze the following Python code with a focus on providing a concise, unbiased overview of its current state. Address each of the following key aspects, keeping descriptions specific to this project. Do not include any code in your responses.

1. **Functionality**: Summarize the code’s main purpose and core functions, focusing on what it aims to achieve.

2. **Organization and Structure**: Describe the structure of modules, classes, and methods, noting how they are organized and interact. Comment on any clear patterns or lack of modularity.

3. **Complexity**: Identify areas that seem complex (e.g., large functions, nested logic). Note overall readability and consistency in naming conventions.

4. **Documentation**: Indicate the level and quality of documentation, including the presence of docstrings and inline comments, and whether they sufficiently explain the code's purpose and usage.

5. **Testing and Reliability**: Note any tests present, describing their scope (e.g., unit or integration tests) and general coverage of the code.

6. **Dependencies**: List key dependencies and briefly describe their role. Note if any dependencies may impact security or maintainability.

**File:** {file_name}

{code}
"""

RECOMMENDATIONS_PROMPT_TEMPLATE = """
Based on the following analysis, provide only the most important, specific, and actionable recommendations to improve this Python code. Focus on high-impact suggestions that address the core areas needing improvement in this particular project. Limit recommendations to those that are clearly achievable and highly relevant. Do not include any code in your responses.

**Analysis:**
{analysis}
"""

SUMMARIZE_PROMPT_TEMPLATE = """
For each of the following recommendations, create a concise, comprehensive paragraph that ensures the recommendation is specific, measurable, achievable, and realistic. Avoid mentioning timelines or the SMART criteria explicitly. Do not include any code in your responses.

{recommendations}
"""

ERROR_ANALYZING_FILE = "[red]Error analyzing {file_name}: {error}[/red]"
ERROR_API_RESPONSE = "[red]Failed to get response for {request_type} of {file_name}. HTTP Status: {status}[/red]"
