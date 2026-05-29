import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import INDEX_PATH


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    content: str
    source: str
    lesson: str | None
    topic: str | None
    kind: str
    keywords: list[str]
    questions: list[str]

    @property
    def searchable_text(self) -> str:
        parts = [
            self.title,
            self.topic or "",
            " ".join(self.keywords),
            " ".join(self.questions),
            self.content,
        ]
        return "\n".join(part for part in parts if part)


def load_documents(path: Path = INDEX_PATH) -> list[Document]:
    if not path.exists():
        raise FileNotFoundError(f"Index not found: {path}. Run `python scripts/build_index.py` first.")

    documents: list[Document] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item: dict[str, Any] = json.loads(line)
            documents.append(
                Document(
                    id=item["id"],
                    title=item.get("title") or item["id"],
                    content=item.get("content") or "",
                    source=item.get("source") or "",
                    lesson=item.get("lesson"),
                    topic=item.get("topic"),
                    kind=item.get("kind") or "text",
                    keywords=item.get("keywords") or [],
                    questions=item.get("questions") or [],
                )
            )
    return documents
