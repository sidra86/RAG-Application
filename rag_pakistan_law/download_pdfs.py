"""
Script to help download Pakistani law PDFs
"""
import os
import requests
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_pdf_directory():
    """Create PDF directory if it doesn't exist"""
    pdf_dir = Path("pdfs")
    pdf_dir.mkdir(exist_ok=True)
    return pdf_dir

def download_file(url, filename, pdf_dir):
    """Download a file from URL"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        file_path = pdf_dir / filename
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        logger.info(f"✅ Downloaded: {filename}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to download {filename}: {e}")
        return False

def main():
    """Main function to guide PDF download"""
    print("📥 Pakistani Law PDF Download Helper")
    print("=" * 50)
    
    # Create PDF directory
    pdf_dir = create_pdf_directory()
    print(f"📁 PDF directory: {pdf_dir.absolute()}")
    
    # Information about required PDFs
    pdf_info = {
        "Pakistan Penal Code": {
            "url": "https://www.pakistancode.gov.pk/english/UY2FqaJw1-apaUY2Fqa-apaUY2Npa5lo-sg-jjjjjjjjjjjjj",
            "filename": "pakistan_penal_code.pdf",
            "description": "Main criminal law document"
        },
        "Constitution of Pakistan": {
            "url": "https://www.na.gov.pk/en/downloads.php",
            "filename": "constitution_1973.pdf", 
            "description": "Fundamental law document"
        }
    }
    
    print("\n📋 Required PDF Documents:")
    print("-" * 30)
    
    for name, info in pdf_info.items():
        print(f"\n📄 {name}")
        print(f"   Description: {info['description']}")
        print(f"   Download URL: {info['url']}")
        print(f"   Save as: {info['filename']}")
        
        # Check if file already exists
        if (pdf_dir / info['filename']).exists():
            print(f"   Status: ✅ Already exists")
        else:
            print(f"   Status: ❌ Not found")
    
    print("\n📝 Instructions:")
    print("1. Visit the URLs above in your browser")
    print("2. Download the PDF files")
    print("3. Save them in the 'pdfs' directory with the correct names")
    print("4. Ensure the PDFs contain selectable text (not just images)")
    
    # Check current status
    print(f"\n📊 Current Status:")
    existing_files = list(pdf_dir.glob("*.pdf"))
    
    if existing_files:
        print(f"✅ Found {len(existing_files)} PDF files:")
        for file in existing_files:
            print(f"   - {file.name}")
    else:
        print("❌ No PDF files found")
    
    print(f"\n🚀 Next Steps:")
    print("1. Download the required PDFs")
    print("2. Run: python test_system.py (to test the system)")
    print("3. Run: streamlit run app.py (to start the application)")

if __name__ == "__main__":
    main()
