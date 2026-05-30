from __future__ import annotations

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
FRONTEND_DIST_DIR = ROOT_DIR / "static"

DEFAULT_TOP_K = 6
MAX_TOP_K = 12

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local").lower()
LOCAL_EMBEDDING_MODEL = os.getenv("LOCAL_EMBEDDING_MODEL", "intfloat/multilingual-e5-small")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
DASHSCOPE_BASE_URL = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-v4")
EMBEDDING_DIMENSIONS = int(os.getenv("EMBEDDING_DIMENSIONS", "1024"))

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv(
    "MYSQL_URL",
    "mysql+aiomysql://course_rag:course_rag@127.0.0.1:3306/course_rag",
)
ADMIN_BOOTSTRAP_USERNAME = os.getenv("ADMIN_BOOTSTRAP_USERNAME", "admin")
ADMIN_BOOTSTRAP_PASSWORD = os.getenv("ADMIN_BOOTSTRAP_PASSWORD")
ADMIN_JWT_SECRET = os.getenv("ADMIN_JWT_SECRET", "change-me")
ADMIN_JWT_EXPIRE_SECONDS = int(os.getenv("ADMIN_JWT_EXPIRE_SECONDS", "86400"))
TOKEN_SESSION_TTL_SECONDS = int(os.getenv("TOKEN_SESSION_TTL_SECONDS", "900"))
TOKEN_HEARTBEAT_INTERVAL_SECONDS = int(os.getenv("TOKEN_HEARTBEAT_INTERVAL_SECONDS", "60"))
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
