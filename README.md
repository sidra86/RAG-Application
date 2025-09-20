# Pakistani Law RAG Assistant

A comprehensive Retrieval-Augmented Generation (RAG) application for searching and understanding Pakistani laws, including the Pakistan Penal Code and Constitution of Pakistan. This application uses Google Gemini for embeddings and text generation, with ChromaDB as the vector database.

## 🎯 Features

- **Document Search**: Ask natural language questions about Pakistani laws
- **Section Lookup**: Direct search by section/article numbers
- **Multi-Document Support**: Search across Pakistan Penal Code and Constitution
- **Intelligent Chunking**: Optimized text processing for better retrieval
- **Web Interface**: User-friendly Streamlit interface
- **Source Attribution**: See which sections your answers come from

## 🛠️ Technology Stack

- **Vector Database**: ChromaDB
- **Embeddings & LLM**: Google Gemini API
- **Web Interface**: Streamlit
- **Text Processing**: PyPDF2, pdfminer.six
- **Python**: 3.8+

## 📋 Prerequisites

1. **Python 3.8 or higher**
2. **Google Gemini API Key** - Get it from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **PDF Documents** - Pakistan Penal Code and Constitution PDFs

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd rag_pakistan_law

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Gemini API key
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Prepare PDF Documents

1. **Download PDFs**:
   - **Pakistan Penal Code**: Visit [pakistancode.gov.pk](https://www.pakistancode.gov.pk/english/UY2FqaJw1-apaUY2Fqa-apaUY2Npa5lo-sg-jjjjjjjjjjjjj)
   - **Constitution of Pakistan**: Visit [na.gov.pk](https://www.na.gov.pk/en/downloads.php)

2. **Place PDFs in the correct directory**:
   ```bash
   mkdir pdfs
   # Copy your PDF files to the pdfs/ directory
   # Name them clearly, e.g., "pakistan_penal_code.pdf", "constitution_1973.pdf"
   ```

### 4. Run the Application

```bash
# Start the Streamlit app
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
rag_pakistan_law/
├── app.py                 # Streamlit web interface
├── rag_system.py         # Main RAG orchestration
├── pdf_processor.py      # PDF text extraction
├── text_chunker.py       # Text chunking and preprocessing
├── vector_store.py       # ChromaDB integration
├── gemini_integration.py # Gemini API integration
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── README.md            # This file
├── pdfs/                # Directory for PDF documents
├── processed_texts/     # Processed text files
└── chroma_db/          # ChromaDB vector database
```

## 🔧 Configuration

Edit `config.py` to customize:

- **Chunk Size**: Default 1000 tokens
- **Chunk Overlap**: Default 200 tokens
- **Database Path**: Default `./chroma_db`
- **Model Settings**: Gemini model configurations

## 📖 Usage Examples

### Natural Language Queries
- "What is the punishment for murder?"
- "What are the fundamental rights in the Constitution?"
- "What constitutes theft under Pakistani law?"
- "What are the duties of a citizen?"

### Section Lookups
- Search for "Section 302" (murder)
- Search for "Article 19" (freedom of speech)
- Search for "Section 420" (cheating)

### Filtering
- Filter by document type (Penal Code or Constitution)
- Adjust number of results returned
- View similarity scores for sources

## 🔄 Database Management

### Rebuilding the Database
If you add new PDFs or want to reprocess existing ones:

1. Go to the sidebar in the web interface
2. Click "🔄 Rebuild Database"
3. Wait for processing to complete

### Resetting the Database
To completely reset the database:

1. Click "🗑️ Reset Database" in the sidebar
2. Rebuild the database with "🔄 Rebuild Database"

## 🐛 Troubleshooting

### Common Issues

1. **"No documents in database"**
   - Ensure PDFs are in the `pdfs/` directory
   - Check that PDFs are readable and contain text
   - Try rebuilding the database

2. **"Gemini API connection failed"**
   - Verify your API key in `.env` file
   - Check your internet connection
   - Ensure you have API credits

3. **"Failed to extract text from PDF"**
   - Try different PDF files
   - Ensure PDFs are not password-protected
   - Check if PDFs contain selectable text

4. **Memory issues with large PDFs**
   - Reduce chunk size in `config.py`
   - Process PDFs one at a time
   - Increase system memory

### Logs
Check the console output for detailed error messages and processing logs.

## 🔒 Legal Disclaimer

This application is for educational and informational purposes only. It should not be considered as legal advice. Always consult with qualified legal professionals for legal matters.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google for the Gemini API
- ChromaDB team for the vector database
- Streamlit for the web framework
- The legal community for making Pakistani laws accessible

## 📞 Support

If you encounter issues or have questions:

1. Check the troubleshooting section
2. Review the logs for error messages
3. Open an issue on GitHub
4. Contact the maintainers

---

**Happy searching through Pakistani laws! ⚖️**
