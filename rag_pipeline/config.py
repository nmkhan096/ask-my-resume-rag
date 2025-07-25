# rag_pipeline/config.py
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from fastembed import TextEmbedding

load_dotenv()

API_KEY = os.environ.get("GROQ_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST", "http://localhost:6333")

# LLM model name
LLM_MODEL_DEFAULT = "llama-3.3-70b-versatile"

# Embedding model
EMBEDDING_MODEL = "jinaai/jina-embeddings-v2-small-en"
EMBEDDING_DIM = 512

# Qdrant client
qd_client = QdrantClient(QDRANT_HOST)
collection_name = "resume-rag"