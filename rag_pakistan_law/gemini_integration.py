"""
Gemini API integration for embeddings and text generation
"""
import google.generativeai as genai
from typing import List, Dict, Any
import logging
from config import GEMINI_API_KEY, EMBEDDING_MODEL, GENERATION_MODEL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiIntegration:
    """Handles Gemini API integration for embeddings and text generation"""
    
    def __init__(self, api_key: str = GEMINI_API_KEY):
        if not api_key:
            raise ValueError("Gemini API key is required")
        
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.embedding_model = genai.GenerativeModel(EMBEDDING_MODEL)
        self.generation_model = genai.GenerativeModel(GENERATION_MODEL)
        
        logger.info("Gemini integration initialized")
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        try:
            embeddings = []
            
            # Process texts in batches to avoid rate limits
            batch_size = 10
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                
                for text in batch:
                    try:
                        # Generate embedding for single text
                        result = self.embedding_model.embed_content(text)
                        embedding = result['embedding']
                        embeddings.append(embedding)
                        
                    except Exception as e:
                        logger.warning(f"Failed to generate embedding for text: {e}")
                        # Add zero vector as fallback
                        embeddings.append([0.0] * 768)  # Standard embedding size
                
                # Small delay between batches
                import time
                time.sleep(0.1)
            
            logger.info(f"Generated {len(embeddings)} embeddings")
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            return []
    
    def generate_answer(self, query: str, context_documents: List[Dict[str, Any]], 
                       max_tokens: int = 1000) -> str:
        """Generate answer using retrieved context documents"""
        try:
            # Prepare context from retrieved documents
            context_text = ""
            for i, doc in enumerate(context_documents[:3]):  # Use top 3 documents
                context_text += f"Document {i+1}:\n"
                context_text += f"Section: {doc['metadata'].get('section_number', 'N/A')}\n"
                context_text += f"Title: {doc['metadata'].get('title', 'N/A')}\n"
                context_text += f"Content: {doc['content']}\n\n"
            
            # Create prompt for Gemini
            prompt = f"""
You are a legal assistant specializing in Pakistani law. Answer the user's question based on the provided legal documents.

Context Documents:
{context_text}

User Question: {query}

Instructions:
1. Provide a clear, accurate answer based on the legal documents provided
2. If the answer is found in a specific section/article, mention the section number
3. If the information is not available in the provided context, say so clearly
4. Use simple language that a non-lawyer can understand
5. If applicable, provide relevant details about punishments, procedures, or requirements

Answer:
"""
            
            # Generate response
            response = self.generation_model.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                return "I apologize, but I couldn't generate a response. Please try rephrasing your question."
                
        except Exception as e:
            logger.error(f"Failed to generate answer: {e}")
            return f"Error generating response: {str(e)}"
    
    def generate_embedding_for_query(self, query: str) -> List[float]:
        """Generate embedding for a user query"""
        try:
            result = self.embedding_model.embed_content(query)
            return result['embedding']
        except Exception as e:
            logger.error(f"Failed to generate query embedding: {e}")
            return []
    
    def test_connection(self) -> bool:
        """Test the Gemini API connection"""
        try:
            test_text = "Test connection"
            embedding = self.generate_embedding_for_query(test_text)
            return len(embedding) > 0
        except Exception as e:
            logger.error(f"Gemini API connection test failed: {e}")
            return False

if __name__ == "__main__":
    # Test the Gemini integration
    if GEMINI_API_KEY:
        gemini = GeminiIntegration()
        if gemini.test_connection():
            print("Gemini API connection successful!")
        else:
            print("Gemini API connection failed!")
    else:
        print("Please set GEMINI_API_KEY in your .env file")
