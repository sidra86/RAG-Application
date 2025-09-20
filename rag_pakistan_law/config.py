"""
Configuration settings for the Pakistani Law RAG application
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ChromaDB Configuration
CHROMA_PERSIST_DIRECTORY = "./chroma_db"
COLLECTION_NAME = "pakistani_laws"

# Text Processing Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Model Configuration
EMBEDDING_MODEL = "models/embedding-001"
GENERATION_MODEL = "gemini-1.5-flash"

# File paths
PDF_DIRECTORY = "./pdfs"
PROCESSED_DIRECTORY = "./processed_texts"
