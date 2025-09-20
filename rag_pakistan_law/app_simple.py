"""
Simplified Streamlit app that handles empty database gracefully
"""
import streamlit as st
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Pakistani Law RAG Assistant",
    page_icon="⚖️",
    layout="wide"
)

def check_setup():
    """Check if the system is properly set up"""
    issues = []
    
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        issues.append("❌ Gemini API key not set. Run: python setup_api_key.py")
    
    # Check for PDFs
    pdf_dir = Path("pdfs")
    if not pdf_dir.exists() or not list(pdf_dir.glob("*.pdf")):
        issues.append("❌ No PDF files found. Run: python setup_directories.py")
    
    # Check for database
    chroma_dir = Path("chroma_db")
    if not chroma_dir.exists():
        issues.append("❌ Database not initialized. Run: python init_database.py")
    
    return issues

def main():
    """Main application function"""
    st.title("⚖️ Pakistani Law RAG Assistant")
    st.markdown("Ask questions about Pakistani laws, including the Pakistan Penal Code and Constitution!")
    
    # Check setup
    issues = check_setup()
    
    if issues:
        st.error("Setup Issues Detected:")
        for issue in issues:
            st.write(issue)
        
        st.markdown("### 🔧 Quick Setup:")
        st.markdown("""
        1. **Get API Key**: Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. **Set API Key**: Run `python setup_api_key.py`
        3. **Initialize Database**: Run `python init_database.py`
        4. **Refresh this page**
        """)
        
        if st.button("🔄 Refresh Page"):
            st.rerun()
        
        return
    
    # Try to load the RAG system
    try:
        from rag_system import PakistaniLawRAG
        
        if 'rag_system' not in st.session_state:
            with st.spinner("Loading RAG system..."):
                st.session_state.rag_system = PakistaniLawRAG()
        
        rag = st.session_state.rag_system
        
        # Check database stats
        try:
            stats = rag.get_database_stats()
            total_docs = stats.get('total_documents', 0)
            
            if total_docs == 0:
                st.warning("⚠️ Database is empty. Please run: `python init_database.py`")
                return
            else:
                st.success(f"✅ Database loaded with {total_docs} documents")
        
        except Exception as e:
            st.error(f"❌ Database error: {e}")
            st.markdown("Please run: `python init_database.py`")
            return
        
        # Main interface
        st.markdown("### 🔍 Ask a Question")
        
        query = st.text_area(
            "Enter your question:",
            placeholder="e.g., What is section 302? What are fundamental rights?",
            height=100
        )
        
        if st.button("🔍 Search", type="primary"):
            if query.strip():
                with st.spinner("Searching..."):
                    result = rag.query(query, n_results=3)
                    
                    if result.get('answer'):
                        st.markdown("### 📖 Answer:")
                        st.write(result['answer'])
                        
                        if result.get('sources'):
                            st.markdown("### 📚 Sources:")
                            for i, source in enumerate(result['sources'], 1):
                                with st.expander(f"Source {i}: {source['title']}"):
                                    st.write(f"**Document Type:** {source['document_type']}")
                                    st.write(f"**Section:** {source['section_number']}")
                                    st.write(f"**Content:** {source['content_preview']}")
                    else:
                        st.error("Sorry, I couldn't find relevant information.")
            else:
                st.warning("Please enter a question.")
        
        # Example questions
        st.markdown("### 💡 Example Questions")
        examples = [
            "What is section 302?",
            "What are fundamental rights?",
            "What is the punishment for theft?",
            "What constitutes murder?"
        ]
        
        cols = st.columns(2)
        for i, example in enumerate(examples):
            with cols[i % 2]:
                if st.button(f"❓ {example}", key=f"example_{i}"):
                    st.session_state.example_query = example
                    st.rerun()
        
        # Handle example query
        if 'example_query' in st.session_state:
            query = st.session_state.example_query
            del st.session_state.example_query
            st.rerun()
    
    except Exception as e:
        st.error(f"❌ Error loading RAG system: {e}")
        st.markdown("Please check your setup and try again.")

if __name__ == "__main__":
    main()
