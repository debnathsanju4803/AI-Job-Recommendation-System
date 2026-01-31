"""
PDF and document parsing utilities
"""
import fitz  # PyMuPDF
from pathlib import Path
from typing import Optional
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    import docx
except ImportError:
    docx = None

from src.utils.logger import logger

class DocumentParser:
    """Parse PDF, DOCX, and text files"""
    
    @staticmethod
    def parse_pdf(file_path: Path) -> str:
        """Extract text from PDF file"""
        try:
            doc = fitz.open(str(file_path))
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            logger.info(f"Successfully parsed PDF: {file_path.name}")
            return text.strip()
        except Exception as e:
            logger.error(f"Error parsing PDF {file_path}: {e}")
            raise
    
    @staticmethod
    def parse_docx(file_path: Path) -> str:
        """Extract text from DOCX file"""
        if docx is None:
            raise ImportError("python-docx not installed. Install with: pip install python-docx")
        try:
            doc = docx.Document(str(file_path))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            logger.info(f"Successfully parsed DOCX: {file_path.name}")
            return text.strip()
        except Exception as e:
            logger.error(f"Error parsing DOCX {file_path}: {e}")
            raise
    
    @staticmethod
    def parse_text(file_path: Path) -> str:
        """Read text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            logger.info(f"Successfully read text file: {file_path.name}")
            return text.strip()
        except Exception as e:
            logger.error(f"Error reading text file {file_path}: {e}")
            raise
    
    @staticmethod
    def parse(file_path: Path) -> str:
        """Parse document based on file extension"""
        suffix = file_path.suffix.lower()
        
        if suffix == '.pdf':
            return DocumentParser.parse_pdf(file_path)
        elif suffix in ['.docx', '.doc']:
            return DocumentParser.parse_docx(file_path)
        elif suffix == '.txt':
            return DocumentParser.parse_text(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
