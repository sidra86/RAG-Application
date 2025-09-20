"""
Streamlit web interface for the Pakistani Law RAG application
"""
import streamlit as st
import os
from rag_system import PakistaniLawRAG
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Pakistani Law RAG Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c5aa0;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .answer-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f4e79;
        margin: 1rem 0;
    }
    .source-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #2c5aa0;
    }
    .error-box {
        background-color: #ffe6e6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #d32f2f;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #4caf50;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_rag_system():
    """Initialize the RAG system"""
    if 'rag_system' not in st.session_state:
        try:
            st.session_state.rag_system = PakistaniLawRAG()
            return True
        except Exception as e:
            st.error(f"Failed to initialize RAG system: {str(e)}")
            return False
    return True

def display_answer(result):
    """Display the answer and sources in a formatted way"""
    if result.get('error'):
        st.markdown(f'<div class="error-box">❌ {result["answer"]}</div>', unsafe_allow_html=True)
        return
    
    # Display answer
    st.markdown(f'<div class="answer-box">📖 <strong>Answer:</strong><br>{result["answer"]}</div>', unsafe_allow_html=True)
    
    # Display sources
    if result.get('sources'):
        st.markdown('<div class="section-header">📚 Sources:</div>', unsafe_allow_html=True)
        for i, source in enumerate(result['sources'], 1):
            with st.expander(f"Source {i}: {source['title']} (Similarity: {source['similarity_score']:.2f})"):
                st.write(f"**Document Type:** {source['document_type']}")
                st.write(f"**Section Number:** {source['section_number']}")
                st.write(f"**Content Preview:** {source['content_preview']}")

def main():
    """Main application function"""
    # Header
    st.markdown('<h1 class="main-header">⚖️ Pakistani Law RAG Assistant</h1>', unsafe_allow_html=True)
    st.markdown("Ask questions about Pakistani laws, including the Pakistan Penal Code and Constitution!")
    
    # Initialize RAG system
    if not initialize_rag_system():
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🔧 Settings")
        
        # Database status
        st.markdown("### Database Status")
        try:
            stats = st.session_state.rag_system.get_database_stats()
            if stats.get('total_documents', 0) > 0:
                st.markdown(f'<div class="success-box">✅ Database loaded<br>Documents: {stats["total_documents"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-box">❌ No documents in database</div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="error-box">❌ Database not accessible</div>', unsafe_allow_html=True)
        
        # Document type filter
        st.markdown("### Filter by Document Type")
        doc_type = st.selectbox(
            "Select document type:",
            ["All", "penal_code", "constitution"],
            help="Filter search results by document type"
        )
        
        # Number of results
        n_results = st.slider(
            "Number of results:",
            min_value=1,
            max_value=10,
            value=5,
            help="Number of similar documents to retrieve"
        )
        
        # Database management
        st.markdown("### Database Management")
        if st.button("🔄 Rebuild Database", help="Rebuild the entire database"):
            with st.spinner("Rebuilding database..."):
                if st.session_state.rag_system.setup_database(force_rebuild=True):
                    st.success("Database rebuilt successfully!")
                    st.rerun()
                else:
                    st.error("Failed to rebuild database")
        
        if st.button("🗑️ Reset Database", help="Reset the entire database"):
            st.session_state.rag_system.reset_database()
            st.success("Database reset successfully!")
            st.rerun()
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["🔍 Ask Questions", "📖 Search by Section", "ℹ️ About"])
    
    with tab1:
        st.markdown('<div class="section-header">Ask a Question</div>', unsafe_allow_html=True)
        
        # Query input
        query = st.text_area(
            "Enter your question:",
            placeholder="e.g., What is the punishment for murder? What are fundamental rights?",
            height=100
        )
        
        # Search button
        if st.button("🔍 Search", type="primary"):
            if query.strip():
                with st.spinner("Searching for relevant information..."):
                    # Determine document type filter
                    doc_filter = None if doc_type == "All" else doc_type
                    
                    # Query the RAG system
                    result = st.session_state.rag_system.query(
                        query, 
                        n_results=n_results,
                        document_type=doc_filter
                    )
                    
                    # Display results
                    display_answer(result)
            else:
                st.warning("Please enter a question.")
        
        # Example questions
        st.markdown("### 💡 Example Questions")
        example_questions = [
            "What is section 302 of the Pakistan Penal Code?",
            "What are the fundamental rights in the Constitution?",
            "What is the punishment for theft?",
            "What are the duties of a citizen?",
            "What constitutes murder under Pakistani law?"
        ]
        
        for i, example in enumerate(example_questions):
            if st.button(f"❓ {example}", key=f"example_{i}"):
                st.session_state.example_query = example
                st.rerun()
        
        # Handle example query
        if 'example_query' in st.session_state:
            query = st.session_state.example_query
            del st.session_state.example_query
            st.rerun()
    
    with tab2:
        st.markdown('<div class="section-header">Search by Section Number</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            section_number = st.text_input(
                "Enter section/article number:",
                placeholder="e.g., 302, 15, 19"
            )
        
        with col2:
            section_doc_type = st.selectbox(
                "Document type:",
                ["Any", "penal_code", "constitution"],
                key="section_doc_type"
            )
        
        if st.button("📖 Find Section", type="primary"):
            if section_number.strip():
                with st.spinner("Searching for section..."):
                    # Determine document type filter
                    doc_filter = None if section_doc_type == "Any" else section_doc_type
                    
                    # Search for section
                    result = st.session_state.rag_system.search_section(
                        section_number.strip(),
                        document_type=doc_filter
                    )
                    
                    # Display results
                    display_answer(result)
            else:
                st.warning("Please enter a section number.")
    
    with tab3:
        st.markdown('<div class="section-header">About This Application</div>', unsafe_allow_html=True)
        
        st.markdown("""
        ### 🎯 Purpose
        This RAG (Retrieval-Augmented Generation) application helps you search and understand Pakistani laws, 
        including the Pakistan Penal Code and the Constitution of Pakistan.
        
        ### 🔧 How It Works
        1. **Document Processing**: PDFs are processed to extract text and identify sections
        2. **Text Chunking**: Large documents are broken into manageable chunks
        3. **Vector Embeddings**: Text chunks are converted to vector embeddings using Google's Gemini
        4. **Vector Storage**: Embeddings are stored in ChromaDB for fast similarity search
        5. **Query Processing**: Your questions are converted to embeddings and matched with relevant content
        6. **Answer Generation**: Gemini generates answers based on the retrieved context
        
        ### 📚 Data Sources
        - **Pakistan Penal Code**: Available from pakistancode.gov.pk
        - **Constitution of Pakistan**: Available from na.gov.pk
        
        ### 🛠️ Technology Stack
        - **Vector Database**: ChromaDB
        - **Embeddings & LLM**: Google Gemini
        - **Web Interface**: Streamlit
        - **Text Processing**: PyPDF2, pdfminer.six
        
        ### 📝 Usage Tips
        - Ask specific questions about legal concepts
        - Use section numbers for direct lookups
        - Filter by document type for targeted searches
        - Check the sources to verify information
        """)
        
        # System information
        st.markdown("### 📊 System Information")
        try:
            stats = st.session_state.rag_system.get_database_stats()
            st.json(stats)
        except:
            st.error("Unable to retrieve system information")

if __name__ == "__main__":
    main()
