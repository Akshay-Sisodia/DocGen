from typing import List
from dataclasses import dataclass

@dataclass
class ChunkConfig:
    """Configuration for code chunking."""
    max_chunk_size: int = 512  # Maximum characters per chunk
    min_chunk_size: int = 128  # Minimum characters per chunk
    overlap: int = 50  # Number of characters to overlap between chunks
    max_chunks_per_file: int = 10  # Maximum number of chunks per file


class CodeChunker:
    """Handles intelligent code chunking."""
    
    def __init__(self, config: ChunkConfig = ChunkConfig()):
        self.config = config
    
    def chunk_code(self, content: str) -> List[str]:
        """
        Intelligently chunk code based on logical boundaries.
        """
        chunks = []
        lines = content.split('\n')
        current_chunk = []
        current_size = 0
        
        def is_boundary(line: str) -> bool:
            """Check if line is a logical boundary in code."""
            boundary_markers = [
                'def ', 'class ', 'if __name__', '# %%', '"""',
                'function ', 'public class', 'export class',
                'interface ', 'struct ', 'void '
            ]
            return any(line.strip().startswith(marker) for marker in boundary_markers)
        
        for line in lines:
            line_size = len(line)
            
            # Check if adding this line would exceed max chunk size
            if current_size + line_size > self.config.max_chunk_size and current_chunk:
                # Only create chunk if it meets minimum size
                if current_size >= self.config.min_chunk_size:
                    chunks.append('\n'.join(current_chunk))
                current_chunk = []
                current_size = 0
            
            # Start new chunk at logical boundaries if current chunk is large enough
            if is_boundary(line) and current_size >= self.config.min_chunk_size:
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                current_chunk = []
                current_size = 0
            
            current_chunk.append(line)
            current_size += line_size
        
        # Add the last chunk if it exists
        if current_chunk and current_size >= self.config.min_chunk_size:
            chunks.append('\n'.join(current_chunk))
        
        # Limit number of chunks per file
        if len(chunks) > self.config.max_chunks_per_file:
            # Keep evenly spaced chunks to maintain coverage
            step = len(chunks) // self.config.max_chunks_per_file
            chunks = chunks[::step][:self.config.max_chunks_per_file]
        
        return chunks