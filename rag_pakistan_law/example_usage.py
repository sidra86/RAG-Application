"""
Example usage of the Pakistani Law RAG system
"""
from rag_system import PakistaniLawRAG
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Example usage of the RAG system"""
    
    # Initialize the RAG system
    print("🚀 Initializing Pakistani Law RAG System...")
    rag = PakistaniLawRAG()
    
    # Setup the database (this will process PDFs and create embeddings)
    print("📚 Setting up database...")
    if not rag.setup_database():
        print("❌ Failed to setup database. Please check your PDFs and API key.")
        return
    
    print("✅ Database setup completed!")
    
    # Example queries
    example_queries = [
        "What is section 302?",
        "What is the punishment for murder?",
        "What are fundamental rights?",
        "What constitutes theft?",
        "What are the duties of a citizen?"
    ]
    
    print("\n🔍 Running example queries...")
    print("=" * 60)
    
    for i, query in enumerate(example_queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 40)
        
        # Query the system
        result = rag.query(query, n_results=3)
        
        # Display results
        print(f"Answer: {result['answer']}")
        
        if result.get('sources'):
            print(f"Sources found: {len(result['sources'])}")
            for j, source in enumerate(result['sources'][:2], 1):  # Show top 2 sources
                print(f"  {j}. {source['title']} (Score: {source['similarity_score']:.2f})")
        
        print()
    
    # Example section search
    print("\n📖 Section Search Examples:")
    print("=" * 60)
    
    section_examples = [
        ("302", "penal_code"),
        ("19", "constitution"),
        ("420", "penal_code")
    ]
    
    for section_num, doc_type in section_examples:
        print(f"\nSearching for Section/Article {section_num} in {doc_type}:")
        print("-" * 40)
        
        result = rag.search_section(section_num, doc_type)
        print(f"Answer: {result['answer'][:200]}...")
        
        if result.get('sources'):
            print(f"Sources found: {len(result['sources'])}")
    
    # Database statistics
    print("\n📊 Database Statistics:")
    print("=" * 60)
    stats = rag.get_database_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
