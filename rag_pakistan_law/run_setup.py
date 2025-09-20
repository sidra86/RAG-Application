"""
Setup script to initialize the Pakistani Law RAG application
"""
import os
import sys
import subprocess
import json
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        "pdfs",
        "processed_texts", 
        "chroma_db"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python version: {sys.version}")

def install_dependencies():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists(".env"):
        with open(".env.example", "r") as f:
            content = f.read()
        with open(".env", "w") as f:
            f.write(content)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env and add your Gemini API key")
    else:
        print("✅ .env file already exists")

def create_sample_pdf_info():
    """Create a file with information about required PDFs"""
    pdf_info = {
        "required_pdfs": [
            {
                "name": "pakistan_penal_code.pdf",
                "source": "https://www.pakistancode.gov.pk/english/UY2FqaJw1-apaUY2Fqa-apaUY2Npa5lo-sg-jjjjjjjjjjjjj",
                "description": "Pakistan Penal Code - Main criminal law document"
            },
            {
                "name": "constitution_1973.pdf", 
                "source": "https://www.na.gov.pk/en/downloads.php",
                "description": "Constitution of Pakistan 1973 - Fundamental law document"
            }
        ],
        "instructions": [
            "1. Download the PDFs from the provided sources",
            "2. Place them in the 'pdfs' directory",
            "3. Ensure the PDFs contain selectable text (not just images)",
            "4. Run the application with: streamlit run app.py"
        ]
    }
    
    with open("pdf_requirements.json", "w") as f:
        json.dump(pdf_info, f, indent=2)
    
    print("✅ Created PDF requirements file")

def main():
    """Main setup function"""
    print("🚀 Setting up Pakistani Law RAG Application...")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Create directories
    create_directories()
    
    # Install dependencies
    install_dependencies()
    
    # Create .env file
    create_env_file()
    
    # Create PDF requirements file
    create_sample_pdf_info()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your Gemini API key")
    print("2. Download PDFs and place them in the 'pdfs' directory")
    print("3. Run the application: streamlit run app.py")
    print("\nFor detailed instructions, see README.md")

if __name__ == "__main__":
    main()
