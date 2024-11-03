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
PROGRESS_FILE_TEXT = "[cyan]Processing[/cyan] [bold yellow]{current_file}[/bold yellow] ([cyan]{current}/{total} files[/cyan])"
PROGRESS_STAGE_TEXT = "[dim]{stage}[/dim]"
PROGRESS_STATUS_TEXT = "[green]✓[/green] {filename} ({status})"

STAGE_ANALYSIS = "analysis"
STAGE_RECOMMENDATIONS = "recommendations" 
STAGE_RANKING = "ranking"
STAGE_SUMMARY = "summary"

ANALYSIS_STAGES = {
    STAGE_ANALYSIS: "[blue]Analyzing code structure[/blue]",
    STAGE_RECOMMENDATIONS: "[yellow]Generating recommendations[/yellow]",
    STAGE_RANKING: "[magenta]Ranking improvements[/magenta]",
    STAGE_SUMMARY: "[green]Summarizing insights[/green]"
}


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
OLLAMA_MODEL_RANKING = "gemma2:9b-instruct-q5_0"

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

RECOMMENDATIONS_PROMPT_TEMPLATE = '''
You are a code improvement assistant. Follow these rules EXACTLY.

TASK:
Analyze the provided code analysis and suggest specific improvements.

FORMAT RULES:
1. Start each recommendation with "RECOMMENDATION:"
2. Follow with "RATIONALE:"
3. End with "OUTCOME:"

EXAMPLE:
RECOMMENDATION: Implement proper error handling in the database connection logic
RATIONALE: Current implementation lacks try-catch blocks for database operations
OUTCOME: Prevent application crashes from database connection failures

REQUIREMENTS:
1. Never include code snippets
2. Never discuss implementation details
3. Focus on architectural and design improvements
4. Be specific but avoid technical details
5. Maximum 5 recommendations
6. Separate each recommendation with blank line
7. Use only the format shown above

Analysis:
{analysis}

Format your response using EXACTLY the structure shown above.
'''

SUMMARIZE_PROMPT_TEMPLATE = '''
You are a technical writing assistant tasked with summarizing code improvement recommendations. You MUST follow these rules EXACTLY.

SUMMARY REQUIREMENTS:
1. Convert each recommendation into a single, comprehensive paragraph
2. Include the specific problem, solution, and expected outcome
3. Use technical but clear language
4. Maintain actionable nature of the recommendation

FORMAT RULES:
- Start each summary with "SUMMARY #X:" (where X is the sequence number)
- Each summary MUST be exactly one paragraph
- Each summary MUST be separated by a blank line
- Maximum 150 words per summary

EXAMPLE:
SUMMARY #1: The implementation of database connection management requires immediate optimization through the introduction of connection pooling. The current approach of creating new connections for each query is causing significant performance bottlenecks and resource wastage. Implementing a connection pool will reduce connection overhead, improve request handling capacity, and ensure more efficient resource utilization across the application.

REQUIREMENTS:
- Do not include any code snippets
- Do not use bullet points or multiple paragraphs
- Do not include any other formatting
- Do not add any additional context or explanation
- Do not use subjective language

Recommendations:
{recommendations}

Format your response using ONLY the structure shown in the example above.
'''

RANKING_PROMPT_TEMPLATE = '''
You are a code review assistant tasked with ranking recommendations. Follow these rules EXACTLY.

YOU MUST:
1. Analyze each input recommendation
2. Assign each one a priority level and impact score
3. Format them according to the EXACT structure below
4. Include justification for each recommendation
5. NEVER include any code snippets or technical implementation details

PRIORITY LEVELS (Choose one):
CRITICAL - Security risks, data loss, crashes
HIGH - Performance issues, maintainability problems
MEDIUM - Code organization, documentation improvements
LOW - Style improvements, minor optimizations

IMPACT SCORING:
5/5 - Prevents system failures or security issues
4/5 - Significantly improves reliability/maintainability
3/5 - Moderately improves code quality
1-2/5 - Minor improvements (these will be filtered out)

OUTPUT FORMAT:
Use EXACTLY this structure (including blank lines):

### CRITICAL

[CRITICAL] (Impact: 5/5) Fix SQL injection vulnerability in user input
- Justification: Current implementation allows malicious SQL injection attacks

### HIGH

[HIGH] (Impact: 4/5) Implement connection pooling
- Justification: Single connection approach causes performance bottlenecks

REQUIREMENTS:
1. Must use exact section headers (### PRIORITY)
2. Must include [PRIORITY] prefix for each recommendation
3. Must include (Impact: X/5) score
4. Must include "- Justification:" line
5. Must separate recommendations with blank lines
6. Never include code snippets or implementation details
7. Never explain or summarize recommendations
8. Never include more than 3 items per priority level
9. Never use Impact scores below 3

Analysis:
{analysis}

Recommendations to Rank:
{recommendations}

Begin output now, using EXACTLY the format shown above.
'''

ERROR_ANALYZING_FILE = "[red]Error analyzing {file_name}: {error}[/red]"
ERROR_API_RESPONSE = "[red]Failed to get response for {request_type} of {file_name}. HTTP Status: {status}[/red]"
