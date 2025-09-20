"""
Quick setup script to create directories and help with PDF download
"""
import os
from pathlib import Path

def create_directories():
    """Create all necessary directories"""
    directories = [
        "pdfs",
        "processed_texts", 
        "chroma_db"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_sample_pdf():
    """Create a sample PDF for testing"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        # Create a sample PDF with some legal content
        c = canvas.Canvas("pdfs/sample_penal_code.pdf", pagesize=letter)
        
        # Add some sample legal content
        c.drawString(100, 750, "PAKISTAN PENAL CODE")
        c.drawString(100, 720, "SAMPLE SECTIONS")
        
        # Section 302
        c.drawString(100, 680, "Section 302 - Punishment for murder")
        c.drawString(100, 660, "Whoever commits murder shall be punished with death,")
        c.drawString(100, 640, "or imprisonment for life, and shall also be liable to fine.")
        
        # Section 420
        c.drawString(100, 600, "Section 420 - Cheating and dishonestly inducing delivery of property")
        c.drawString(100, 580, "Whoever cheats and thereby dishonestly induces the person")
        c.drawString(100, 560, "deceived to deliver any property to any person, or to make,")
        c.drawString(100, 540, "alter or destroy the whole or any part of a valuable security,")
        c.drawString(100, 520, "shall be punished with imprisonment of either description")
        c.drawString(100, 500, "for a term which may extend to seven years, and shall also be liable to fine.")
        
        c.save()
        print("✅ Created sample PDF: pdfs/sample_penal_code.pdf")
        
    except ImportError:
        print("⚠️  reportlab not installed. Creating text file instead...")
        with open("pdfs/sample_penal_code.txt", "w") as f:
            f.write("""
PAKISTAN PENAL CODE - SAMPLE SECTIONS

Section 302 - Punishment for murder
Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.

Section 420 - Cheating and dishonestly inducing delivery of property
Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.

Section 379 - Theft
Whoever, intending to take dishonestly any moveable property out of the possession of any person without that person's consent, moves that property in order to such taking, is said to commit theft.
            """)
        print("✅ Created sample text file: pdfs/sample_penal_code.txt")

def main():
    """Main setup function"""
    print("🔧 Setting up Pakistani Law RAG directories...")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Create sample PDF
    create_sample_pdf()
    
    print("\n📋 Next steps:")
    print("1. Download real PDFs from:")
    print("   - Pakistan Penal Code: https://www.pakistancode.gov.pk/")
    print("   - Constitution: https://www.na.gov.pk/en/downloads.php")
    print("2. Place them in the 'pdfs' directory")
    print("3. Run: python test_system.py")
    print("4. Run: streamlit run app.py")

if __name__ == "__main__":
    main()
