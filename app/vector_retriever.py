from __future__ import annotations

import numpy as np

from .config import INDEX_DIR, MAX_TOP_K
from .corpus import Document
from .embeddings import create_embedder
from .query_expansion import contains_cjk, expand_query, looks_english_document

EMBEDDINGS_PATH = INDEX_DIR / "embeddings.npz"


class VectorRetriever:
    def __init__(self, documents: list[Document]) -> None:
        if not EMBEDDINGS_PATH.exists():
            raise FileNotFoundError(f"Vector index not found: {EMBEDDINGS_PATH}. Run `uv run python scripts/build_embeddings.py` first.")
        data = np.load(EMBEDDINGS_PATH, allow_pickle=False)
        self.documents = documents
        self.embeddings = data["embeddings"].astype(np.float32)
        doc_ids = data["doc_ids"].astype(str).tolist()
        document_ids = [doc.id for doc in documents]
        if doc_ids != document_ids:
            raise ValueError("Vector index does not match documents.jsonl. Rebuild.")
        self.embedder = create_embedder()

        # Pre-compute mask for English PDF documents
        self._english_pdf_mask = np.array([
            looks_english_document(doc.kind, doc.content, doc.title)
            for doc in documents
        ], dtype=bool)

    def search(self, query: str, top_k: int) -> list[tuple[Document, float]]:
        top_k = min(top_k, MAX_TOP_K, len(self.documents))
        expanded_query = expand_query(query)
        query_embedding = self.embedder.encode_query(expanded_query)
        scores = self.embeddings @ query_embedding

        if contains_cjk(query) and self._english_pdf_mask.any():
            return self._mixed_search(scores, top_k)
        return self._simple_topk(scores, top_k)

    def _simple_topk(self, scores: np.ndarray, top_k: int) -> list[tuple[Document, float]]:
        indices = np.argpartition(-scores, range(top_k))[:top_k]
        ranked = sorted(indices, key=lambda idx: float(scores[idx]), reverse=True)
        return [(self.documents[int(idx)], float(scores[idx])) for idx in ranked[:top_k]]

    def _mixed_search(self, scores: np.ndarray, top_k: int) -> list[tuple[Document, float]]:
        min_english = 2 if top_k >= 6 else 1

        # Top overall results (deduplicated by source)
        general_k = max(top_k * 10, 60)
        general_indices = np.argpartition(-scores, range(min(general_k, len(scores))))[:general_k]
        general_ranked = sorted(general_indices, key=lambda idx: float(scores[idx]), reverse=True)

        selected: list[int] = []
        seen_sources: set[str] = set()
        for idx in general_ranked:
            doc = self.documents[int(idx)]
            source_key = f"{doc.kind}:{doc.source}"
            if source_key in seen_sources and len(selected) >= max(3, top_k // 2):
                continue
            selected.append(int(idx))
            seen_sources.add(source_key)
            if len(selected) >= top_k:
                break

        # Top English PDF results
        en_pdf_indices = np.where(self._english_pdf_mask)[0]
        if en_pdf_indices.size > 0:
            en_scores = scores[en_pdf_indices]
            top_en_count = min(max(4, top_k), len(en_pdf_indices))
            top_en_local = np.argpartition(-en_scores, range(top_en_count))[:top_en_count]
            top_en_ranked = sorted(top_en_local, key=lambda idx: float(en_scores[idx]), reverse=True)

            current_english = sum(
                1 for idx in selected
                if self._english_pdf_mask[int(idx)]
            )
            added = 0
            seen_en_sources: set[str] = set()
            for local_idx in top_en_ranked:
                if current_english + added >= min_english:
                    break
                global_idx = int(en_pdf_indices[local_idx])
                doc = self.documents[global_idx]
                source_key = f"{doc.source}:{doc.title}"
                if source_key in seen_en_sources:
                    continue
                seen_en_sources.add(source_key)
                if global_idx in selected:
                    added += 1
                    continue
                # Insert English PDF by replacing lowest-scored non-English result
                replace_at = len(selected) - 1
                while replace_at >= 0 and self._english_pdf_mask[selected[replace_at]]:
                    replace_at -= 1
                if replace_at >= 0:
                    selected[replace_at] = global_idx
                    added += 1

        # Final sort by score
        selected.sort(key=lambda idx: float(scores[idx]), reverse=True)
        return [(self.documents[idx], float(scores[idx])) for idx in selected[:top_k]]
