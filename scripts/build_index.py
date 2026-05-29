import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAG_INDEX = ROOT / "data" / "processed" / "rag_corpus" / "index.jsonl"
PDF_DIR = ROOT / "data" / "processed" / "pdf_markdown"
OUT_DIR = ROOT / "data" / "index"
OUT_PATH = OUT_DIR / "documents.jsonl"


def clean_text(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_markdown(text: str, source: str, max_chars: int = 1400) -> list[dict]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks = []
    current = []
    current_len = 0
    for paragraph in paragraphs:
        if current and current_len + len(paragraph) > max_chars:
            chunks.append("\n\n".join(current))
            current = []
            current_len = 0
        current.append(paragraph)
        current_len += len(paragraph)
    if current:
        chunks.append("\n\n".join(current))

    docs = []
    for index, content in enumerate(chunks, 1):
        title = next((line.strip("# ") for line in content.splitlines() if line.strip().startswith("#")), None)
        docs.append(
            {
                "id": f"pdf::{Path(source).stem}::{index:03d}",
                "title": title or f"{Path(source).stem} 第 {index} 段",
                "content": clean_text(content),
                "source": source,
                "lesson": None,
                "topic": Path(source).stem,
                "kind": "pdf_markdown",
                "keywords": [Path(source).stem],
                "questions": [],
            }
        )
    return docs


def load_rag_docs() -> list[dict]:
    docs = []
    with RAG_INDEX.open("r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            docs.append(
                {
                    "id": f"course::{item['chunk_id']}",
                    "title": item.get("title") or item["chunk_id"],
                    "content": clean_text(item.get("content") or ""),
                    "source": item.get("source_file") or "",
                    "lesson": item.get("lesson"),
                    "topic": item.get("topic"),
                    "kind": "video_transcript_rag",
                    "keywords": item.get("keywords") or [],
                    "questions": item.get("questions") or [],
                }
            )
    return docs


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    docs = load_rag_docs()
    for path in sorted(PDF_DIR.glob("*.md")):
        docs.extend(chunk_markdown(path.read_text(encoding="utf-8"), path.name))

    with OUT_PATH.open("w", encoding="utf-8") as f:
        for doc in docs:
            if doc["content"]:
                f.write(json.dumps(doc, ensure_ascii=False) + "\n")

    print(json.dumps({"documents": len(docs), "output": str(OUT_PATH)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
