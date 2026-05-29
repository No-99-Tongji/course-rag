import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

DATA_DIR = ROOT_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
RAG_CORPUS_DIR = PROCESSED_DIR / "rag_corpus"
PDF_MARKDOWN_DIR = PROCESSED_DIR / "pdf_markdown"
INDEX_DIR = DATA_DIR / "index"
INDEX_PATH = INDEX_DIR / "documents.jsonl"
EMBEDDINGS_PATH = INDEX_DIR / "embeddings.npz"

DEFAULT_TOP_K = 6
MAX_TOP_K = 12

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local").lower()
LOCAL_EMBEDDING_MODEL = os.getenv("LOCAL_EMBEDDING_MODEL", "intfloat/multilingual-e5-small")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
DASHSCOPE_BASE_URL = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-v4")
EMBEDDING_DIMENSIONS = int(os.getenv("EMBEDDING_DIMENSIONS", "1024"))
