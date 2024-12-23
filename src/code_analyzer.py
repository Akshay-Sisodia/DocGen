import ast
import chardet
import lizard
from typing import List, Dict
from src.chunker import CodeMetrics

class CodeAnalyzer:
    """Advanced code analysis for multiple programming languages."""
    
    SUPPORTED_EXTENSIONS = {
        'Python': ['.py'],
        'JavaScript/TypeScript': ['.js', '.jsx', '.ts', '.tsx'],
        'Java': ['.java'],
        'C/C++': ['.c', '.cpp', '.h', '.hpp'],
        'Ruby': ['.rb'],
        'Go': ['.go'],
        'Rust': ['.rs'],
        'PHP': ['.php'],
        'C#': ['.cs'],
        'Swift': ['.swift']
    }
    
    def analyze_code_complexity(self, file_path: str) -> CodeMetrics:
        """Analyze code complexity metrics using a structured return type."""
        try:
            with open(file_path, 'rb') as file:
                encoding = chardet.detect(file.read())['encoding']

            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
                
            analysis = lizard.analyze_file(file_path)
            
            return CodeMetrics(
                cyclomatic_complexity=analysis.average_cyclomatic_complexity,
                nloc=analysis.nloc,
                function_count=len(analysis.function_list),
                avg_lines_per_function=analysis.average_nloc,
                functions=[{
                    'name': func.name,
                    'complexity': func.cyclomatic_complexity,
                    'nloc': func.nloc,
                    'parameters': len(func.parameters),
                    'start_line': func.start_line,
                    'end_line': func.end_line
                } for func in analysis.function_list]
            )
        except Exception as e:
            raise ValueError(f"Error analyzing {file_path}: {str(e)}")
