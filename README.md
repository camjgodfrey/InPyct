
# InPyct 🔍

**InPyct** is a lightweight AI-powered Python project analysis tool that leverages local LLMs through Ollama to provide insightful code analysis and actionable recommendations. It combines project structure visualisation with AI-driven code review, helping developers understand and improve their Python projects.

![Apache License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)

## Features 🚀

### Project Analysis
- **File System Analysis**: Recursively analyses project directories while ignoring common excludes (hidden files, `__pycache__`)
- **Rich Terminal UI**: Displays analysis results in an interactive, colour-coded tree view of files and directories
- **Detailed Statistics**: Provides comprehensive metrics about your project structure, including:
  - Total number of directories
  - Total number of files
  - Python file count
  - Visualisation of the file hierarchy

### AI-Powered Insights
- **Flexible LLM Support**: Compatible with any language model available through Ollama
- **Three-Stage Analysis Pipeline**:
  1. Initial code analysis, focusing on functionality and structure
  2. Generation of detailed recommendations
  3. SMART (Specific, Measurable, Achievable, Realistic, Timely) recommendation summarisation

### User Experience
- **Progress Tracking**: Real-time progress indicators during analysis
- **Error Handling**: Graceful management of common issues, such as:
  - Invalid directories
  - API connection issues
  - File reading errors
- **Asynchronous Processing**: Efficient, parallel processing of multiple files

## Installation 🛠️

### Prerequisites
1. Python 3.x
2. Ollama with your preferred language models installed

```bash
# Install your preferred Ollama models
ollama pull <model-name>

# Clone the repository
git clone https://github.com/yourusername/inpyct.git
cd inpyct

# Install dependencies
pip install -r requirements.txt
```

## Usage 📚

1. Start the Ollama server:
   ```bash
   ollama serve
   ```

2. Run InPyct:
   ```bash
   python -m src.main
   ```

3. Enter the path to your Python project when prompted.

## Project Structure 📂

```
src/
├── __init__.py           # Package initialisation
├── analyser.py           # Core analysis engine and directory traversal
├── api_integration.py    # Ollama API integration and prompt management
├── constants.py          # Configuration and message templates
├── display.py            # Terminal UI components using Rich
├── helper.py             # Utility functions and error handling
├── main.py               # Application entry point
└── models.py             # Data models for analysis results
```

## Development Roadmap 🗺️

### Potential Features
1. **Enhanced Analysis**
   - Code complexity metrics
   - Dependency analysis
   - Test coverage reporting
   - Documentation coverage assessment

2. **AI Capabilities**
   - Custom model support beyond Ollama
   - Fine-tuned recommendation generation
   - Code refactoring suggestions
   - Security vulnerability detection

3. **User Interface**
   - Web interface option
   - Interactive recommendation review
   - Batch project analysis
   - Export results in multiple formats

4. **Integration Options**
   - Git integration for change tracking
   - CI/CD pipeline integration
   - IDE plugin support
   - Team collaboration features

## Contributing 🤝

We warmly welcome contributions, especially from first-time contributors. Whether you're experienced or new to open source, your insights and improvements are valuable to us. Here are a few ways you can help:

1. **Code Contributions**
   - Implement new analysis features
   - Improve error handling
   - Optimise performance
   - Add test coverage
   - We’re happy to help guide newcomers to open source!

2. **Documentation**
   - Enhance installation instructions
   - Add usage examples
   - Create tutorials
   - Translate documentation
   - Clarify confusing sections or fix typos

3. **Testing**
   - Report bugs
   - Suggest improvements
   - Test with various project sizes
   - Validate recommendations
   - Experiment with different Ollama models and share your results

## Licence 📄

InPyct is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

---

Built with ❤️ using Python and AI to help you better understand your code.

