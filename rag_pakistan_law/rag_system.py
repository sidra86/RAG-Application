"""
Main RAG system that orchestrates all components
"""
import os
import json
from typing import List, Dict, Any, Optional
import logging
from pdf_processor import PDFProcessor
from text_chunker import TextChunker
from vector_store import VectorStore
from gemini_integration import GeminiIntegration
from config import PDF_DIRECTORY, PROCESSED_DIRECTORY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PakistaniLawRAG:
    """Main RAG system for Pakistani law documents"""
    
    def __init__(self):
        self.pdf_processor = PDFProcessor(PDF_DIRECTORY)
        self.text_chunker = TextChunker()
        self.vector_store = VectorStore()
        self.gemini = GeminiIntegration()
        
        # Check if data is already processed
        self.processed_file = os.path.join(PROCESSED_DIRECTORY, "sections.json")
        
    def setup_database(self, force_rebuild: bool = False):
        """Set up the vector database with processed documents"""
        try:
            # Check if database already has data
            stats = self.vector_store.get_collection_stats()
            if stats.get('total_documents', 0) > 0 and not force_rebuild:
                logger.info("Database already contains documents. Use force_rebuild=True to rebuild.")
                return True
            
            # Process PDFs if not already done
            if not os.path.exists(self.processed_file) or force_rebuild:
                logger.info("Processing PDF documents...")
                sections = self.pdf_processor.process_all_pdfs()
                
                if not sections:
                    logger.error("No sections found in PDFs. Please check your PDF files.")
                    return False
                
                # Save processed sections
                os.makedirs(PROCESSED_DIRECTORY, exist_ok=True)
                with open(self.processed_file, 'w', encoding='utf-8') as f:
                    json.dump(sections, f, indent=2, ensure_ascii=False)
                
                logger.info(f"Processed {len(sections)} sections from PDFs")
            else:
                # Load existing processed sections
                with open(self.processed_file, 'r', encoding='utf-8') as f:
                    sections = json.load(f)
                logger.info(f"Loaded {len(sections)} existing sections")
            
            # Create chunks from sections
            logger.info("Creating text chunks...")
            chunks = self.text_chunker.create_chunks(sections)
            chunks_with_metadata = self.text_chunker.add_metadata(chunks)
            
            # Generate embeddings
            logger.info("Generating embeddings...")
            texts = [chunk['content'] for chunk in chunks_with_metadata]
            embeddings = self.gemini.generate_embeddings(texts)
            
            if not embeddings:
                logger.error("Failed to generate embeddings")
                return False
            
            # Add to vector store
            logger.info("Adding documents to vector store...")
            self.vector_store.add_documents(chunks_with_metadata, embeddings)
            
            logger.info("Database setup completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup database: {e}")
            return False
    
    def query(self, question: str, n_results: int = 5, 
              document_type: Optional[str] = None) -> Dict[str, Any]:
        """Query the RAG system with a question"""
        try:
            # Generate embedding for the question
            query_embedding = self.gemini.generate_embedding_for_query(question)
            if not query_embedding:
                return {
                    'answer': 'Sorry, I could not process your question.',
                    'sources': [],
                    'error': 'Failed to generate query embedding'
                }
            
            # Search for similar documents
            filter_metadata = None
            if document_type:
                filter_metadata = {'document_type': document_type}
            
            similar_docs = self.vector_store.search_similar(
                query_embedding, 
                n_results=n_results,
                filter_metadata=filter_metadata
            )
            
            if not similar_docs:
                return {
                    'answer': 'I could not find relevant information to answer your question.',
                    'sources': [],
                    'error': 'No relevant documents found'
                }
            
            # Generate answer using retrieved context
            answer = self.gemini.generate_answer(question, similar_docs)
            
            # Prepare sources
            sources = []
            for doc in similar_docs:
                source = {
                    'section_number': doc['metadata'].get('section_number', 'N/A'),
                    'title': doc['metadata'].get('title', 'N/A'),
                    'document_type': doc['metadata'].get('document_type', 'N/A'),
                    'similarity_score': doc['similarity_score'],
                    'content_preview': doc['content'][:200] + "..." if len(doc['content']) > 200 else doc['content']
                }
                sources.append(source)
            
            return {
                'answer': answer,
                'sources': sources,
                'query': question
            }
            
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return {
                'answer': f'Sorry, an error occurred while processing your question: {str(e)}',
                'sources': [],
                'error': str(e)
            }
    
    def search_section(self, section_number: str, document_type: str = None) -> Dict[str, Any]:
        """Search for a specific section by number"""
        try:
            results = self.vector_store.search_by_section(section_number, document_type)
            
            if not results:
                return {
                    'answer': f'Section {section_number} not found.',
                    'sources': [],
                    'error': 'Section not found'
                }
            
            # Combine all chunks for the section
            combined_content = ""
            for result in results:
                combined_content += result['content'] + "\n\n"
            
            # Generate a summary answer
            answer = f"Here is the content of Section {section_number}:\n\n{combined_content}"
            
            # Prepare sources
            sources = []
            for result in results:
                source = {
                    'section_number': result['metadata'].get('section_number', 'N/A'),
                    'title': result['metadata'].get('title', 'N/A'),
                    'document_type': result['metadata'].get('document_type', 'N/A'),
                    'content_preview': result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
                }
                sources.append(source)
            
            return {
                'answer': answer,
                'sources': sources,
                'query': f'Section {section_number}'
            }
            
        except Exception as e:
            logger.error(f"Section search failed: {e}")
            return {
                'answer': f'Error searching for section {section_number}: {str(e)}',
                'sources': [],
                'error': str(e)
            }
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the database"""
        return self.vector_store.get_collection_stats()
    
    def reset_database(self):
        """Reset the entire database"""
        try:
            self.vector_store.reset_collection()
            if os.path.exists(self.processed_file):
                os.remove(self.processed_file)
            logger.info("Database reset successfully")
        except Exception as e:
            logger.error(f"Failed to reset database: {e}")

if __name__ == "__main__":
    # Test the RAG system
    rag = PakistaniLawRAG()
    
    # Setup database
    if rag.setup_database():
        print("Database setup successful!")
        
        # Test query
        result = rag.query("What is section 302?")
        print(f"Query result: {result['answer']}")
        
        # Test section search
        section_result = rag.search_section("302", "penal_code")
        print(f"Section 302: {section_result['answer'][:200]}...")
    else:
        print("Database setup failed!")
