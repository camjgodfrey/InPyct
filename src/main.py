import asyncio
from rich.console import Console
from analyser import CodeAnalyzer
from display import DisplayManager
from helper import (
    display_message,
    display_welcome,
    display_goodbye,
    prompt_directory,
    handle_analysis_error,
)
from constants import NO_PYTHON_FILES_MESSAGE


async def main():
    console = Console()
    analyzer = CodeAnalyzer()
    display_manager = DisplayManager()

    display_welcome(console)

    while True:
        try:
            directory = await prompt_directory(console)
            if directory is None:
                display_goodbye(console)
                break

            analysis = await analyzer.analyze_directory(directory)
            if analysis.total_files > 0:
                display_manager.display_tree(analysis)
            else:
                display_message(console, NO_PYTHON_FILES_MESSAGE, border_style="red")
        except KeyboardInterrupt:
            display_goodbye(console)
            break
        except Exception as e:
            handle_analysis_error(console, e)


if __name__ == "__main__":
    asyncio.run(main())
