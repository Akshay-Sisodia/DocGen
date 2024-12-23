from pathlib import Path
import streamlit as st
import tempfile
import os
import shutil
import requests
from src.git_repo_handler import GitRepoHandler
from src.documentation import CodeDocumentation


class StreamlitUI:
    """Enhanced Streamlit UI with Git support."""
    
    def __init__(self):
        self.documentation = None
        self.model_url = "http://localhost:11434/api/tags"
        self.file_extensions = ['.py', '.js', '.java', '.cpp', '.h', '.tsx', '.jsx', '.ts']
        self.available_models = self.fetch_available_models()
    
    def fetch_available_models(self) -> list:
        """Fetch models from the API and return a list of model names."""
        try:
            response = requests.get(self.model_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            models_data = response.json()
            
            # Extract model names
            model_names = [model['name'] for model in models_data.get('models', [])]
            return model_names if model_names else ["No models available"]
        except requests.RequestException as e:
            st.error(f"Error fetching models from the API: {e}")
            return ["Error fetching models"]

    def render_source_input(self) -> None:
        """Render input options for code source."""
        source_type = st.radio(
            "Select Source Type",
            ["Files", "Folder", "Git Repository"]
        )
        
        if source_type == "Files":
            return st.file_uploader(
                "Upload Project Files",
                accept_multiple_files=True,
                type=[ext[1:] for ext in self.file_extensions]
            )
        elif source_type == "Folder":
            folder_path = st.text_input("Enter folder path:")
            if folder_path and os.path.isdir(folder_path):
                return folder_path
        else:
            repo_url = st.text_input("Enter Git repository URL:")
            if repo_url and GitRepoHandler.is_git_url(repo_url):
                return repo_url
        
        return None
    
    def handle_source_input(self, source: str, model: str, extensions: list) -> None:
        """Handle different types of source inputs."""
        with tempfile.TemporaryDirectory() as temp_dir:
            if isinstance(source, list):  # Files
                for file in source:
                    with open(Path(temp_dir) / file.name, 'wb') as f:
                        f.write(file.getvalue())
            elif GitRepoHandler.is_git_url(source):  # Git repository
                GitRepoHandler.clone_repo(source, temp_dir)
            else:  # Folder path
                shutil.copytree(source, temp_dir, dirs_exist_ok=True)
            
            self.documentation = CodeDocumentation(temp_dir, model_name=model)
            self.documentation.load_documents(file_extensions=extensions)
            st.success("Source loaded successfully!")
