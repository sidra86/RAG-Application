"""
Main entry point for the Pakistani Law RAG application
"""
import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("❌ .env file not found. Please run: python run_setup.py")
        return False
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not set in .env file")
        return False
    
    # Check if PDFs exist
    pdf_dir = Path("pdfs")
    if not pdf_dir.exists() or not list(pdf_dir.glob("*.pdf")):
        print("⚠️  No PDF files found in pdfs/ directory")
        print("   Please download PDFs and run: python download_pdfs.py")
        return False
    
    print("✅ All requirements met!")
    return True

def main():
    """Main function"""
    print("⚖️  Pakistani Law RAG Application")
    print("=" * 40)
    
    if not check_requirements():
        print("\n❌ Requirements not met. Please fix the issues above.")
        return
    
    print("\n🚀 Starting the application...")
    print("   The app will open in your browser at http://localhost:8501")
    print("   Press Ctrl+C to stop the application")
    
    try:
        # Run Streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error running application: {e}")

if __name__ == "__main__":
    main()
