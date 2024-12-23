# DocGen - Advanced Code Documentation Assistant

DocGen is an intelligent code documentation and analysis tool that leverages LLM capabilities to help developers understand, document, and analyze their codebase. It supports multiple programming languages and provides an interactive web interface for querying code documentation.

## Features

- **Intelligent Code Analysis**: Automatically analyzes code complexity and structure across multiple programming languages
- **Interactive Documentation**: Ask questions about your codebase in natural language
- **Multi-Source Support**: Load code from:
  - Local files
  - Project folders
  - Git repositories
- **Multiple Language Support**: Compatible with various programming languages including:
  - Python
  - JavaScript/TypeScript
  - Java
  - C/C++
  - Ruby
  - Go
  - Rust
  - PHP
  - C#
  - Swift
- **Smart Code Chunking**: Intelligently breaks down code into manageable pieces while preserving context
- **Vector Search**: Utilizes embeddings for efficient code documentation search
- **User-Friendly Interface**: Built with Streamlit for an intuitive user experience

## System Requirements

- Python 3.8+
- [Ollama](https://ollama.ai/) running locally
- Git (for repository cloning features)
- Sufficient RAM for code analysis and embedding generation

## Quick Start

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure Ollama is running locally with the required models:
```bash
ollama pull codellama
ollama pull snowflake-arctic-embed
```

3. Start the application:
```bash
streamlit run app.py
```

4. Open your browser and navigate to the provided local URL (typically http://localhost:8501)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, feature requests, or questions, please open an issue in the repository.