from __future__ import annotations

from collections.abc import Iterable

import numpy as np
from openai import OpenAI
from sentence_transformers import SentenceTransformer

from .config import (
    DASHSCOPE_API_KEY,
    DASHSCOPE_BASE_URL,
    EMBEDDING_DIMENSIONS,
    EMBEDDING_MODEL,
    EMBEDDING_PROVIDER,
    LOCAL_EMBEDDING_MODEL,
    ROOT_DIR,
)

LOCAL_MODEL_PATH = ROOT_DIR / "models" / "multilingual-e5-small"


def get_embedding_provider() -> str:
    if EMBEDDING_PROVIDER == "qwen":
        if not DASHSCOPE_API_KEY:
            raise RuntimeError("EMBEDDING_PROVIDER=qwen requires DASHSCOPE_API_KEY in .env")
        return "qwen"
    return "local"


class LocalEmbedder:
    def __init__(self) -> None:
        model_name = str(LOCAL_MODEL_PATH) if LOCAL_MODEL_PATH.exists() else LOCAL_EMBEDDING_MODEL
        self.model = SentenceTransformer(model_name)
        self.model_name = LOCAL_EMBEDDING_MODEL

    def encode_documents(self, texts: list[str]) -> np.ndarray:
        return self.model.encode(
            ["passage: " + text for text in texts],
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=True,
            convert_to_numpy=True,
        ).astype(np.float32)

    def encode_query(self, query: str) -> np.ndarray:
        return self.model.encode(
            ["query: " + query],
            normalize_embeddings=True,
            convert_to_numpy=True,
        ).astype(np.float32)[0]


class QwenEmbedder:
    def __init__(self) -> None:
        if not DASHSCOPE_API_KEY:
            raise RuntimeError("DASHSCOPE_API_KEY is required for Qwen embeddings")
        self.client = OpenAI(api_key=DASHSCOPE_API_KEY, base_url=DASHSCOPE_BASE_URL)
        self.model_name = EMBEDDING_MODEL

    def encode_documents(self, texts: list[str]) -> np.ndarray:
        vectors = []
        for batch in batched(texts, 10):
            vectors.extend(self._embed(batch))
        return normalize(np.array(vectors, dtype=np.float32))

    def encode_query(self, query: str) -> np.ndarray:
        return normalize(np.array(self._embed([query])[0], dtype=np.float32))

    def _embed(self, texts: list[str]) -> list[list[float]]:
        kwargs = {}
        if EMBEDDING_DIMENSIONS:
            kwargs["dimensions"] = EMBEDDING_DIMENSIONS
        response = self.client.embeddings.create(model=EMBEDDING_MODEL, input=texts, **kwargs)
        return [item.embedding for item in response.data]


def create_embedder() -> LocalEmbedder | QwenEmbedder:
    if get_embedding_provider() == "qwen":
        return QwenEmbedder()
    return LocalEmbedder()


def normalize(array: np.ndarray) -> np.ndarray:
    if array.ndim == 1:
        norm = np.linalg.norm(array)
        return array if norm == 0 else (array / norm).astype(np.float32)
    norms = np.linalg.norm(array, axis=1, keepdims=True)
    norms[norms == 0] = 1
    return (array / norms).astype(np.float32)


def batched(items: list[str], size: int) -> Iterable[list[str]]:
    for index in range(0, len(items), size):
        yield items[index : index + size]
