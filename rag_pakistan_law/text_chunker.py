"""
Text chunking module for preparing text for vector embeddings
"""
import re
from typing import List, Dict
import tiktoken
from config import CHUNK_SIZE, CHUNK_OVERLAP

class TextChunker:
    """Handles text chunking for optimal embedding generation"""
    
    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken"""
        return len(self.encoding.encode(text))
    
    def split_text_by_tokens(self, text: str) -> List[str]:
        """Split text into chunks based on token count"""
        tokens = self.encoding.encode(text)
        chunks = []
        
        start = 0
        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoding.decode(chunk_tokens)
            chunks.append(chunk_text)
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            if start >= len(tokens):
                break
        
        return chunks
    
    def split_text_by_sentences(self, text: str) -> List[str]:
        """Split text into chunks by sentences for better semantic coherence"""
        # Split by sentences (period, exclamation, question mark)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Check if adding this sentence would exceed chunk size
            test_chunk = current_chunk + " " + sentence if current_chunk else sentence
            
            if self.count_tokens(test_chunk) <= self.chunk_size:
                current_chunk = test_chunk
            else:
                # Save current chunk and start new one
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def create_chunks(self, sections: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Create chunks from processed sections"""
        all_chunks = []
        
        for section in sections:
            content = section['content']
            
            # If content is small enough, use as single chunk
            if self.count_tokens(content) <= self.chunk_size:
                chunk = {
                    'id': f"{section['document_type']}_{section['section_number']}_0",
                    'section_number': section['section_number'],
                    'title': section['title'],
                    'content': content,
                    'document_type': section['document_type'],
                    'chunk_index': 0,
                    'total_chunks': 1
                }
                all_chunks.append(chunk)
            else:
                # Split into multiple chunks
                chunks = self.split_text_by_sentences(content)
                
                for i, chunk_text in enumerate(chunks):
                    chunk = {
                        'id': f"{section['document_type']}_{section['section_number']}_{i}",
                        'section_number': section['section_number'],
                        'title': f"{section['title']} (Part {i+1})",
                        'content': chunk_text,
                        'document_type': section['document_type'],
                        'chunk_index': i,
                        'total_chunks': len(chunks)
                    }
                    all_chunks.append(chunk)
        
        return all_chunks
    
    def add_metadata(self, chunks: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Add additional metadata to chunks for better retrieval"""
        for chunk in chunks:
            # Add searchable keywords
            keywords = self.extract_keywords(chunk['content'])
            chunk['keywords'] = keywords
            
            # Add content summary
            chunk['summary'] = self.create_summary(chunk['content'])
            
            # Add legal context
            chunk['legal_context'] = self.determine_legal_context(chunk)
        
        return chunks
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        # Common legal terms and important words
        legal_terms = [
            'punishment', 'offence', 'penalty', 'fine', 'imprisonment', 'death',
            'murder', 'theft', 'fraud', 'assault', 'defamation', 'perjury',
            'constitution', 'fundamental', 'rights', 'duties', 'citizen',
            'government', 'parliament', 'judiciary', 'executive'
        ]
        
        # Convert to lowercase for matching
        text_lower = text.lower()
        found_keywords = []
        
        for term in legal_terms:
            if term in text_lower:
                found_keywords.append(term)
        
        # Also extract section/article numbers mentioned
        numbers = re.findall(r'\b\d+[A-Z]?\b', text)
        found_keywords.extend(numbers)
        
        return list(set(found_keywords))
    
    def create_summary(self, text: str) -> str:
        """Create a brief summary of the chunk content"""
        # Take first 200 characters as summary
        summary = text[:200].strip()
        if len(text) > 200:
            summary += "..."
        return summary
    
    def determine_legal_context(self, chunk: Dict[str, str]) -> str:
        """Determine the legal context of the chunk"""
        content = chunk['content'].lower()
        doc_type = chunk['document_type']
        
        if doc_type == 'penal_code':
            if any(word in content for word in ['murder', 'death', 'kill']):
                return 'criminal_law_homicide'
            elif any(word in content for word in ['theft', 'steal', 'robbery']):
                return 'criminal_law_property'
            elif any(word in content for word in ['assault', 'hurt', 'injury']):
                return 'criminal_law_violence'
            else:
                return 'criminal_law_general'
        
        elif doc_type == 'constitution':
            if any(word in content for word in ['fundamental', 'rights', 'freedom']):
                return 'constitutional_rights'
            elif any(word in content for word in ['government', 'parliament', 'executive']):
                return 'constitutional_government'
            elif any(word in content for word in ['judiciary', 'court', 'judge']):
                return 'constitutional_judiciary'
            else:
                return 'constitutional_general'
        
        return 'general_legal'

if __name__ == "__main__":
    # Test the chunker
    chunker = TextChunker()
    
    # Sample section for testing
    sample_section = {
        'section_number': '302',
        'title': 'Section 302',
        'content': 'Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.',
        'document_type': 'penal_code'
    }
    
    chunks = chunker.create_chunks([sample_section])
    chunks_with_metadata = chunker.add_metadata(chunks)
    
    print("Sample chunk:")
    print(chunks_with_metadata[0])
