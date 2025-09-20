"""
Test script to verify the Pakistani Law RAG system components
"""
import os
import sys
import logging
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import GEMINI_API_KEY
from pdf_processor import PDFProcessor
from text_chunker import TextChunker
from vector_store import VectorStore
from gemini_integration import GeminiIntegration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_config():
    """Test configuration loading"""
    print("🔧 Testing configuration...")
    
    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not found in environment")
        return False
    
    print("✅ Configuration loaded successfully")
    return True

def test_pdf_processor():
    """Test PDF processor"""
    print("\n📄 Testing PDF processor...")
    
    try:
        processor = PDFProcessor()
        
        # Check if PDF directory exists
        if not os.path.exists("./pdfs"):
            print("⚠️  PDF directory not found. Creating it...")
            os.makedirs("./pdfs")
        
        # List PDFs in directory
        pdf_files = [f for f in os.listdir("./pdfs") if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print("⚠️  No PDF files found in ./pdfs directory")
            print("   Please add PDF files to test PDF processing")
            return True  # Not a failure, just no files to process
        
        print(f"✅ Found {len(pdf_files)} PDF files")
        return True
        
    except Exception as e:
        print(f"❌ PDF processor test failed: {e}")
        return False

def test_text_chunker():
    """Test text chunker"""
    print("\n✂️  Testing text chunker...")
    
    try:
        chunker = TextChunker()
        
        # Test with sample text
        sample_text = "This is a sample legal text. " * 100  # Create long text
        chunks = chunker.split_text_by_sentences(sample_text)
        
        print(f"✅ Text chunker working. Created {len(chunks)} chunks")
        return True
        
    except Exception as e:
        print(f"❌ Text chunker test failed: {e}")
        return False

def test_vector_store():
    """Test vector store"""
    print("\n🗄️  Testing vector store...")
    
    try:
        vector_store = VectorStore()
        stats = vector_store.get_collection_stats()
        
        print(f"✅ Vector store connected. Documents: {stats.get('total_documents', 0)}")
        return True
        
    except Exception as e:
        print(f"❌ Vector store test failed: {e}")
        return False

def test_gemini_integration():
    """Test Gemini integration"""
    print("\n🤖 Testing Gemini integration...")
    
    try:
        gemini = GeminiIntegration()
        
        if gemini.test_connection():
            print("✅ Gemini API connection successful")
            return True
        else:
            print("❌ Gemini API connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Gemini integration test failed: {e}")
        return False

def test_dependencies():
    """Test if all required packages are installed"""
    print("\n📦 Testing dependencies...")
    
    required_packages = [
        'google.generativeai',
        'chromadb',
        'PyPDF2',
        'pdfminer',
        'streamlit',
        'tiktoken',
        'numpy',
        'pandas'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Testing Pakistani Law RAG System Components")
    print("=" * 60)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Configuration", test_config),
        ("PDF Processor", test_pdf_processor),
        ("Text Chunker", test_text_chunker),
        ("Vector Store", test_vector_store),
        ("Gemini Integration", test_gemini_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
    else:
        print("⚠️  Some tests failed. Please fix the issues before running the application.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
