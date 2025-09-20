"""
Initialize the database with sample data
"""
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_system import PakistaniLawRAG
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Initialize the database"""
    print("🚀 Initializing Pakistani Law RAG Database...")
    print("=" * 50)
    
    try:
        # Initialize RAG system
        rag = PakistaniLawRAG()
        
        # Check if we have PDFs
        pdf_dir = Path("pdfs")
        pdf_files = list(pdf_dir.glob("*.pdf"))
        
        if not pdf_files:
            print("❌ No PDF files found in pdfs/ directory")
            print("   Please add PDF files or run: python setup_directories.py")
            return False
        
        print(f"📄 Found {len(pdf_files)} PDF files:")
        for pdf in pdf_files:
            print(f"   - {pdf.name}")
        
        # Setup database
        print("\n📚 Setting up database...")
        success = rag.setup_database(force_rebuild=True)
        
        if success:
            print("✅ Database initialized successfully!")
            
            # Get stats
            stats = rag.get_database_stats()
            print(f"📊 Database contains {stats.get('total_documents', 0)} documents")
            
            # Test a simple query
            print("\n🧪 Testing with sample query...")
            result = rag.query("What is section 302?")
            
            if result.get('answer'):
                print("✅ Sample query successful!")
                print(f"Answer: {result['answer'][:100]}...")
            else:
                print("⚠️  Sample query failed, but database is ready")
            
            return True
        else:
            print("❌ Failed to initialize database")
            return False
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Database is ready! You can now run: streamlit run app.py")
    else:
        print("\n❌ Database initialization failed. Please check the errors above.")
