"""
Vector store module using ChromaDB for storing and retrieving legal document embeddings
"""
import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import logging
from config import CHROMA_PERSIST_DIRECTORY, COLLECTION_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    """Manages vector storage and retrieval using ChromaDB"""
    
    def __init__(self, persist_directory: str = CHROMA_PERSIST_DIRECTORY):
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(self.persist_directory, exist_ok=True)
            
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            try:
                self.collection = self.client.get_collection(name=COLLECTION_NAME)
                logger.info(f"Loaded existing collection: {COLLECTION_NAME}")
            except ValueError:
                # Collection doesn't exist, create it
                self.collection = self.client.create_collection(
                    name=COLLECTION_NAME,
                    metadata={"description": "Pakistani Law Documents"}
                )
                logger.info(f"Created new collection: {COLLECTION_NAME}")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise
    
    def add_documents(self, chunks: List[Dict[str, str]], embeddings: List[List[float]]):
        """Add document chunks with embeddings to the vector store"""
        try:
            # Prepare data for ChromaDB
            ids = [chunk['id'] for chunk in chunks]
            documents = [chunk['content'] for chunk in chunks]
            metadatas = []
            
            for chunk in chunks:
                metadata = {
                    'section_number': chunk['section_number'],
                    'title': chunk['title'],
                    'document_type': chunk['document_type'],
                    'chunk_index': chunk['chunk_index'],
                    'total_chunks': chunk['total_chunks'],
                    'keywords': ', '.join(chunk.get('keywords', [])),
                    'summary': chunk.get('summary', ''),
                    'legal_context': chunk.get('legal_context', 'general_legal')
                }
                metadatas.append(metadata)
            
            # Add to collection
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )
            
            logger.info(f"Added {len(chunks)} documents to vector store")
            
        except Exception as e:
            logger.error(f"Failed to add documents to vector store: {e}")
            raise
    
    def search_similar(self, query_embedding: List[float], n_results: int = 5, 
                      filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar documents using vector similarity"""
        try:
            # Prepare where clause for filtering
            where_clause = None
            if filter_metadata:
                where_clause = filter_metadata
            
            # Perform similarity search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_clause,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['ids'][0])):
                result = {
                    'id': results['ids'][0][i],
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'similarity_score': 1 - results['distances'][0][i]  # Convert distance to similarity
                }
                formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to search vector store: {e}")
            return []
    
    def search_by_section(self, section_number: str, document_type: str = None) -> List[Dict[str, Any]]:
        """Search for specific section by number"""
        try:
            where_clause = {'section_number': section_number}
            if document_type:
                where_clause['document_type'] = document_type
            
            results = self.collection.query(
                query_texts=[""],  # Empty query since we're filtering by metadata
                n_results=10,
                where=where_clause,
                include=['documents', 'metadatas']
            )
            
            formatted_results = []
            for i in range(len(results['ids'][0])):
                result = {
                    'id': results['ids'][0][i],
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i]
                }
                formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to search by section: {e}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection"""
        try:
            count = self.collection.count()
            return {
                'total_documents': count,
                'collection_name': COLLECTION_NAME,
                'persist_directory': self.persist_directory
            }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {}
    
    def delete_collection(self):
        """Delete the entire collection (use with caution)"""
        try:
            self.client.delete_collection(name=COLLECTION_NAME)
            logger.info(f"Deleted collection: {COLLECTION_NAME}")
        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
    
    def reset_collection(self):
        """Reset the collection (delete and recreate)"""
        try:
            self.delete_collection()
            self._initialize_client()
            logger.info("Collection reset successfully")
        except Exception as e:
            logger.error(f"Failed to reset collection: {e}")

if __name__ == "__main__":
    # Test the vector store
    vector_store = VectorStore()
    stats = vector_store.get_collection_stats()
    print(f"Collection stats: {stats}")
