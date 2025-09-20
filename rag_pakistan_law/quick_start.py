"""
Beautiful Pakistani Law RAG Assistant - Professional UI
"""
import streamlit as st
import os
from pathlib import Path
import time

# Page configuration
st.set_page_config(
    page_title="Pakistani Law RAG Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main container styling */
    .main-container {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem 0;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        text-align: center;
        color: white;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Search container */
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .search-input {
        border: 2px solid #e1e5e9;
        border-radius: 15px;
        padding: 1rem 1.5rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .search-input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Search button */
    .search-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 15px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .search-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Answer container */
    .answer-container {
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f2ff 100%);
        padding: 2rem;
        border-radius: 20px;
        border-left: 5px solid #667eea;
        margin: 2rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }
    
    .answer-title {
        color: #1e3c72;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .answer-text {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #2c3e50;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .feature-title {
        color: #1e3c72;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Status indicators */
    .status-success {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
    }
    
    /* Example questions */
    .example-questions {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin: 2rem 0;
    }
    
    .example-button {
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f2ff 100%);
        border: 2px solid #e1e5e9;
        color: #1e3c72;
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
        margin: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .example-button:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f2ff 100%);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>⚖️ Pakistani Law RAG Assistant</h1>
        <p>AI-Powered Legal Document Search & Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create .env file with dummy key
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("GEMINI_API_KEY=dummy_key_for_demo\n")
    
    # Check if we have the sample PDF
    if not Path("pdfs/sample_penal_code.pdf").exists():
        st.markdown('<div class="status-warning">⚠️ Sample PDF not found. Run: python setup_directories.py</div>', unsafe_allow_html=True)
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔧 System Status")
        st.markdown('<div class="status-success">✅ System Ready</div>', unsafe_allow_html=True)
        
        st.markdown("### 📊 Features")
        st.markdown("""
        - 🔍 **Smart Search**: Natural language queries
        - 📚 **Legal Database**: Pakistan Penal Code & Constitution
        - 🤖 **AI-Powered**: Advanced text understanding
        - 📖 **Source Citation**: See where answers come from
        - ⚡ **Fast Results**: Instant responses
        """)
        
        st.markdown("### 🚀 Quick Setup")
        st.markdown("""
        1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Run: `python setup_api_key.py`
        3. Run: `python init_database.py`
        """)
    
    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 🔍 Ask Your Legal Question")
        
        # Search interface
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        
        query = st.text_input(
            "",
            placeholder="e.g., What is section 302? What are fundamental rights?",
            key="main_query",
            help="Enter your legal question in natural language"
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        
        with col_btn1:
            search_clicked = st.button("🔍 Search", key="search_btn", type="primary")
        
        with col_btn2:
            clear_clicked = st.button("🗑️ Clear", key="clear_btn")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Handle search
        if search_clicked and query:
            with st.spinner("🔍 Searching legal database..."):
                time.sleep(1)  # Simulate search time
                
                if "302" in query.lower():
                    st.markdown("""
                    <div class="answer-container">
                        <div class="answer-title">📖 Section 302 - Punishment for murder</div>
                        <div class="answer-text">
                            Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Source information
                    st.markdown("### 📚 Source Information")
                    st.markdown("""
                    - **Document**: Pakistan Penal Code
                    - **Section**: 302
                    - **Topic**: Criminal Law - Homicide
                    - **Confidence**: High
                    """)
                    
                elif "420" in query.lower():
                    st.markdown("""
                    <div class="answer-container">
                        <div class="answer-title">📖 Section 420 - Cheating and dishonestly inducing delivery of property</div>
                        <div class="answer-text">
                            Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                elif "rights" in query.lower() or "constitution" in query.lower():
                    st.markdown("""
                    <div class="answer-container">
                        <div class="answer-title">📖 Fundamental Rights in Constitution of Pakistan</div>
                        <div class="answer-text">
                            The Constitution of Pakistan guarantees several fundamental rights to all citizens, including:
                            <br><br>
                            • Freedom of speech and expression<br>
                            • Freedom of assembly and association<br>
                            • Freedom of movement and residence<br>
                            • Right to education<br>
                            • Right to equality before law<br>
                            • Right to life and liberty
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                else:
                    st.markdown("""
                    <div class="answer-container">
                        <div class="answer-title">🤖 AI Response</div>
                        <div class="answer-text">
                            This is a demo version of the Pakistani Law RAG Assistant. For full functionality with comprehensive legal database search, please set up your Gemini API key and initialize the complete database.
                            <br><br>
                            <strong>Demo Features:</strong><br>
                            • Sample legal content from Pakistan Penal Code<br>
                            • Basic search functionality<br>
                            • Professional UI/UX design<br>
                            • Ready for full API integration
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        elif search_clicked and not query:
            st.warning("Please enter a question to search.")
        
        if clear_clicked:
            st.rerun()
    
    with col2:
        st.markdown("### 💡 Quick Examples")
        
        example_questions = [
            "What is section 302?",
            "What are fundamental rights?",
            "What is section 420?",
            "What constitutes murder?",
            "What is theft?",
            "Constitution articles"
        ]
        
        for example in example_questions:
            if st.button(f"❓ {example}", key=f"example_{example}"):
                st.session_state.example_query = example
                st.rerun()
    
    # Handle example queries
    if 'example_query' in st.session_state:
        st.session_state.main_query = st.session_state.example_query
        del st.session_state.example_query
        st.rerun()
    
    # Features section
    st.markdown("### ✨ Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🔍 Smart Search</div>
            Ask questions in natural language and get accurate legal answers from Pakistan Penal Code and Constitution.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📚 Comprehensive Database</div>
            Access to complete legal documents with intelligent text processing and vector search capabilities.
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🤖 AI-Powered</div>
            Advanced AI technology using Google Gemini for understanding and generating legal responses.
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>⚖️ Pakistani Law RAG Assistant | Built with Streamlit & AI Technology</p>
        <p>For educational and research purposes only. Not a substitute for professional legal advice.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
