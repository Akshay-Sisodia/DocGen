# DocGen Setup Guide

This guide provides detailed instructions for setting up and running DocGen on your system.

## Prerequisites

### Required Software

1. **Python Environment**:
   - Python 3.8 or higher
   - pip (Python package installer)
   - venv or conda for virtual environment management

2. **Ollama**:
   - Install from [ollama.ai](https://ollama.ai/)
   - Required for LLM functionality and embeddings

3. **Git**:
   - Required for repository cloning features
   - Install from [git-scm.com](https://git-scm.com/)

## Installation Steps

1. **Create and Activate Virtual Environment**:
   ```bash
   # Using venv
   python -m venv docgen-env
   
   # On Windows
   docgen-env\Scripts\activate
   
   # On Unix or MacOS
   source docgen-env/bin/activate
   ```

2. **Clone the Repository**:
   ```bash
   git clone http://www.github.com/Akshay-Sisodia/DocGen
   cd docgen
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Required Ollama Models**:
   ```bash
   # Pull the required models
   ollama pull codellama
   ollama pull snowflake-arctic-embed
   ```

## Configuration

### Required Python Packages

Create a `requirements.txt` file with the following dependencies:
```
streamlit
git-python
chardet
lizard
llama-index
requests
```

### Environment Setup

1. Ensure Ollama is running:
   ```bash
   # Start Ollama service
   ollama serve
   ```

2. Verify the Ollama API is accessible at:
   ```
   http://localhost:11434/api/tags
   ```

## Running DocGen

1. **Start the Application**:
   ```bash
   streamlit run app.py
   ```

2. **Access the Web Interface**:
   - Open your browser
   - Navigate to `http://localhost:8501`

## Troubleshooting

### Common Issues

1. **Ollama Connection Error**:
   - Ensure Ollama is running (`ollama serve`)
   - Check if the API is accessible at the default port
   - Verify firewall settings

2. **Memory Issues**:
   - Increase available RAM
   - Reduce batch size in code processing
   - Monitor system resources during operation

3. **File Permission Issues**:
   - Ensure write permissions in the temporary directory
   - Check file ownership in the project directory

### Getting Help

1. Check the error messages in the terminal
2. Review the application logs
3. Open an issue in the repository with:
   - Error message
   - Steps to reproduce
   - System information
   - Relevant logs

## Security Considerations

1. **Local Development**:
   - The application runs locally by default
   - No sensitive data is sent to external services
   - Code analysis is performed on your machine

2. **File Access**:
   - The application needs read access to source code
   - Temporary files are created during analysis
   - Clean-up is automatic after processing

## Maintenance

1. **Updating Dependencies**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Updating Ollama Models**:
   ```bash
   ollama pull codellama:latest
   ollama pull snowflake-arctic-embed:latest
   ```

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Ollama Documentation](https://ollama.ai/docs)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
