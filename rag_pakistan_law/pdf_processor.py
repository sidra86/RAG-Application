"""
PDF processing module for extracting text from Pakistani law documents
"""
import os
import re
from typing import List, Dict, Tuple
import PyPDF2
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFProcessor:
    """Handles PDF text extraction and preprocessing for Pakistani laws"""
    
    def __init__(self, pdf_directory: str = "./pdfs"):
        self.pdf_directory = pdf_directory
        self.processed_texts = []
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using multiple methods for better accuracy"""
        try:
            # Method 1: Try pdfminer first (better for complex layouts)
            text = extract_text(pdf_path, laparams=LAParams())
            if text.strip():
                return text
        except Exception as e:
            logger.warning(f"pdfminer failed for {pdf_path}: {e}")
        
        try:
            # Method 2: Fallback to PyPDF2
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            logger.error(f"PyPDF2 also failed for {pdf_path}: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers/footers
        text = re.sub(r'Page \d+ of \d+', '', text)
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        
        # Clean up common PDF artifacts
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\(\)\[\]\{\}\-\'\"\/]', '', text)
        
        return text.strip()
    
    def extract_sections(self, text: str, document_type: str) -> List[Dict[str, str]]:
        """Extract individual sections from the document"""
        sections = []
        
        if document_type.lower() == "penal_code":
            # Pattern for Pakistan Penal Code sections
            section_pattern = r'Section\s+(\d+[A-Z]?)\s*[:\-]?\s*(.*?)(?=Section\s+\d+[A-Z]?|$)'
            matches = re.finditer(section_pattern, text, re.DOTALL | re.IGNORECASE)
            
            for match in matches:
                section_num = match.group(1).strip()
                section_text = match.group(2).strip()
                
                if section_text and len(section_text) > 50:  # Filter out very short sections
                    sections.append({
                        'section_number': section_num,
                        'title': f"Section {section_num}",
                        'content': self.clean_text(section_text),
                        'document_type': 'penal_code'
                    })
        
        elif document_type.lower() == "constitution":
            # Pattern for Constitution articles
            article_pattern = r'Article\s+(\d+[A-Z]?)\s*[:\-]?\s*(.*?)(?=Article\s+\d+[A-Z]?|$)'
            matches = re.finditer(article_pattern, text, re.DOTALL | re.IGNORECASE)
            
            for match in matches:
                article_num = match.group(1).strip()
                article_text = match.group(2).strip()
                
                if article_text and len(article_text) > 50:
                    sections.append({
                        'section_number': article_num,
                        'title': f"Article {article_num}",
                        'content': self.clean_text(article_text),
                        'document_type': 'constitution'
                    })
        
        return sections
    
    def process_pdf(self, pdf_path: str, document_type: str) -> List[Dict[str, str]]:
        """Process a single PDF file and extract sections"""
        logger.info(f"Processing {pdf_path} as {document_type}")
        
        # Extract text
        raw_text = self.extract_text_from_pdf(pdf_path)
        if not raw_text:
            logger.error(f"Failed to extract text from {pdf_path}")
            return []
        
        # Clean text
        cleaned_text = self.clean_text(raw_text)
        
        # Extract sections
        sections = self.extract_sections(cleaned_text, document_type)
        
        logger.info(f"Extracted {len(sections)} sections from {pdf_path}")
        return sections
    
    def process_all_pdfs(self) -> List[Dict[str, str]]:
        """Process all PDFs in the directory"""
        all_sections = []
        
        if not os.path.exists(self.pdf_directory):
            logger.warning(f"PDF directory {self.pdf_directory} does not exist")
            return all_sections
        
        for filename in os.listdir(self.pdf_directory):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(self.pdf_directory, filename)
                
                # Determine document type based on filename
                if 'penal' in filename.lower() or 'ppc' in filename.lower():
                    doc_type = 'penal_code'
                elif 'constitution' in filename.lower():
                    doc_type = 'constitution'
                else:
                    doc_type = 'unknown'
                
                sections = self.process_pdf(pdf_path, doc_type)
                all_sections.extend(sections)
        
        self.processed_texts = all_sections
        logger.info(f"Total sections processed: {len(all_sections)}")
        return all_sections
    
    def save_processed_texts(self, output_file: str = "./processed_texts/sections.json"):
        """Save processed sections to a file"""
        import json
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.processed_texts, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Processed texts saved to {output_file}")

if __name__ == "__main__":
    processor = PDFProcessor()
    sections = processor.process_all_pdfs()
    processor.save_processed_texts()
