"""
Document loader utilities for AI classifier
Handles PDF, DOCX, and TXT files
"""
from pathlib import Path
from typing import List, Dict
import PyPDF2
from docx import Document
import pdfplumber

class DocumentLoader:
    """Load and extract text from various document formats"""
    
    @staticmethod
    def load_pdf_pypdf(file_path: str) -> str:
        """Load PDF using PyPDF2"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error loading PDF with PyPDF2: {e}")
            return ""
    
    @staticmethod
    def load_pdf_pdfplumber(file_path: str) -> str:
        """Load PDF using pdfplumber (better for tables)"""
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error loading PDF with pdfplumber: {e}")
            return ""
    
    @staticmethod
    def load_docx(file_path: str) -> str:
        """Load DOCX file"""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            print(f"Error loading DOCX: {e}")
            return ""
    
    @staticmethod
    def load_txt(file_path: str) -> str:
        """Load TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error loading TXT: {e}")
            return ""
    
    @staticmethod
    def load_document(file_path: str) -> str:
        """
        Load document based on file extension
        Returns extracted text or empty string if failed
        """
        path = Path(file_path)
        extension = path.suffix.lower()
        
        if extension == '.pdf':
            # Try pdfplumber first (better quality), fallback to PyPDF2
            text = DocumentLoader.load_pdf_pdfplumber(file_path)
            if not text:
                text = DocumentLoader.load_pdf_pypdf(file_path)
            return text
        
        elif extension == '.docx':
            return DocumentLoader.load_docx(file_path)
        
        elif extension == '.txt':
            return DocumentLoader.load_txt(file_path)
        
        else:
            print(f"Unsupported file type: {extension}")
            return ""
    
    @staticmethod
    def load_directory(directory: str, label: str) -> List[Dict[str, str]]:
        """
        Load all supported documents from a directory
        Returns list of dicts: {text, metadata}
        """
        documents = []
        directory_path = Path(directory)
        
        if not directory_path.exists():
            print(f"Directory not found: {directory}")
            return documents
        
        # Supported extensions
        extensions = ('.pdf', '.docx', '.txt')
        
        for file_path in directory_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in extensions:
                print(f"Loading: {file_path.name}")
                
                text = DocumentLoader.load_document(str(file_path))
                
                if text:
                    documents.append({
                        'text': text,
                        'metadata': {
                            'source': str(file_path),
                            'filename': file_path.name,
                            'label': label,
                            'extension': file_path.suffix.lower()
                        }
                    })
                else:
                    print(f"Failed to extract text from: {file_path.name}")
        
        return documents
