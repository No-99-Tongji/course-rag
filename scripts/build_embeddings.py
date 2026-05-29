import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np

from app.config import EMBEDDING_PROVIDER, EMBEDDINGS_PATH, INDEX_PATH
from app.embeddings import create_embedder

DOCS_PATH = ROOT / "data" / "index" / "documents.jsonl"


def load_docs() -> list[dict]:
    docs = []
    with DOCS_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                docs.append(json.loads(line))
    return docs


def embedding_text(doc: dict) -> str:
    parts = [
        doc.get("title") or "",
        doc.get("topic") or "",
        " ".join(doc.get("keywords") or []),
        " ".join(doc.get("questions") or []),
        doc.get("content") or "",
    ]
    return "\n".join(part for part in parts if part)


def main() -> None:
    if not INDEX_PATH.exists():
        raise FileNotFoundError(f"Run `uv run python scripts/build_index.py` first.")
    docs = load_docs()
    embedder = create_embedder()
    texts = [embedding_text(doc) for doc in docs]
    embeddings = embedder.encode_documents(texts)
    EMBEDDINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        EMBEDDINGS_PATH,
        embeddings=embeddings,
        doc_ids=np.array([doc["id"] for doc in docs]),
        provider=np.array([EMBEDDING_PROVIDER]),
        model=np.array([getattr(embedder, "model_name", "unknown")]),
    )
    print(json.dumps({
        "documents": len(docs),
        "dimensions": int(embeddings.shape[1]),
        "provider": EMBEDDING_PROVIDER,
        "model": getattr(embedder, "model_name", "unknown"),
        "output": str(EMBEDDINGS_PATH),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
