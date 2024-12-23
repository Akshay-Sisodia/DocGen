from concurrent.futures import ThreadPoolExecutor
import os
from typing import List, Optional

import concurrent
from src.chunker import CodeChunker
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.node_parser import CodeSplitter


class CodeDocumentation:
    """Handles code documentation with simplified chunking."""
    
    def __init__(self, source_dir: str, model_name: str = "codellama"):
        self.source_dir = source_dir
        self.model_name = model_name
        self.index = None
    
    def process_file(self, file_path: str) -> List[str]:
        """Process a single file into simplified chunks."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return self.simple_chunk_code(content)
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            return []

    def simple_chunk_code(self, content: str) -> List[str]:
        """Simplified chunking of code based on max chunk size."""
        chunks = []
        lines = content.split('\n')
        current_chunk = []
        current_size = 0
        max_chunk_size = 512  # Max size in characters per chunk
        min_chunk_size = 128  # Min size in characters per chunk

        for line in lines:
            line_size = len(line)
            
            # Check if adding this line would exceed max chunk size
            if current_size + line_size > max_chunk_size and current_chunk:
                if current_size >= min_chunk_size:  # Only add chunk if it meets min size
                    chunks.append('\n'.join(current_chunk))
                current_chunk = []
                current_size = 0
            
            current_chunk.append(line)
            current_size += line_size
        
        # Add the last chunk if it exists
        if current_chunk and current_size >= min_chunk_size:
            chunks.append('\n'.join(current_chunk))
        
        return chunks
    
    def load_documents(self, file_extensions: Optional[List[str]] = None) -> None:
        """Load and index documents with simplified chunking."""  
        if file_extensions is None:
            file_extensions = ['.py', '.js', '.java', '.cpp', '.h', '.tsx', '.jsx', '.ts']
        
        all_files = []
        for root, _, files in os.walk(self.source_dir):
            for file in files:
                if any(file.endswith(ext) for ext in file_extensions):
                    all_files.append(os.path.join(root, file))
        
        # Process files in parallel
        documents = []
        with ThreadPoolExecutor() as executor:
            future_to_file = {executor.submit(self.process_file, file): file 
                            for file in all_files}
            
            for future in concurrent.futures.as_completed(future_to_file):
                try:
                    file_chunks = future.result()
                    for chunk in file_chunks:
                        print(f"Processing chunk: {chunk[:200]}...")  # Print the first 200 characters of the chunk
                    documents.extend(Document(text=chunk) for chunk in file_chunks)
                except Exception as exc:
                    file = future_to_file[future]
                    print(f'{file} generated an exception: {exc}')

        embed_model = OllamaEmbedding(model_name='snowflake-arctic-embed')
        # Create index without parsing the content
        self.index = VectorStoreIndex.from_documents(documents, node_parser=CodeSplitter,embed_model=embed_model)
    
    def query_documentation(self, query: str) -> str:
        """Query the documentation index."""
        if self.index is None:
            return "Documentation not loaded."
        query_engine = self.index.as_query_engine(llm=Ollama(model='llama3.2'))
        response = query_engine.query(query)
        return str(response)
