import jieba
from rank_bm25 import BM25Okapi

from .corpus import Document


class Retriever:
    def __init__(self, documents: list[Document]) -> None:
        self.documents = documents
        self.tokenized = [self._tokenize(doc.searchable_text) for doc in documents]
        self.bm25 = BM25Okapi(self.tokenized)

    def search(self, query: str, top_k: int) -> list[tuple[Document, float]]:
        tokens = self._tokenize(query)
        scores = self.bm25.get_scores(tokens)
        ranked = sorted(enumerate(scores), key=lambda item: item[1], reverse=True)
        results: list[tuple[Document, float]] = []
        for index, score in ranked[:top_k]:
            if score <= 0 and results:
                continue
            results.append((self.documents[index], float(score)))
        return results

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        tokens = []
        for token in jieba.cut_for_search(text.lower()):
            token = token.strip()
            if len(token) > 1:
                tokens.append(token)
        return tokens
