from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .config import DEFAULT_TOP_K, MAX_TOP_K, ROOT_DIR
from .corpus import Document, load_documents
from .qa import answer_with_optional_llm
from .vector_retriever import VectorRetriever


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    top_k: int = Field(DEFAULT_TOP_K, ge=1, le=MAX_TOP_K)


class SearchResult(BaseModel):
    id: str
    title: str
    source: str
    lesson: str | None
    topic: str | None
    kind: str
    keywords: list[str]
    questions: list[str]
    content: str
    score: float


class AskResponse(BaseModel):
    answer: str
    sources: list[SearchResult]


documents: list[Document] = []
retriever: VectorRetriever | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global documents, retriever
    documents = load_documents()
    retriever = VectorRetriever(documents)
    yield


app = FastAPI(title="Course RAG", version="0.1.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=ROOT_DIR / "static"), name="static")


def to_result(doc: Document, score: float) -> SearchResult:
    return SearchResult(
        id=doc.id,
        title=doc.title,
        source=doc.source,
        lesson=doc.lesson,
        topic=doc.topic,
        kind=doc.kind,
        keywords=doc.keywords,
        questions=doc.questions,
        content=doc.content,
        score=score,
    )


@app.get("/")
def home() -> FileResponse:
    return FileResponse(ROOT_DIR / "static" / "index.html")


@app.get("/health")
def health() -> dict[str, int | str]:
    return {"status": "ok", "documents": len(documents)}


@app.get("/api/search", response_model=list[SearchResult])
def search(
    q: Annotated[str, Query(min_length=1, max_length=1000)],
    top_k: Annotated[int, Query(ge=1, le=MAX_TOP_K)] = DEFAULT_TOP_K,
) -> list[SearchResult]:
    if retriever is None:
        raise HTTPException(status_code=503, detail="Retriever is not ready")
    return [to_result(doc, score) for doc, score in retriever.search(q, top_k)]


@app.post("/api/ask", response_model=AskResponse)
async def ask(request: AskRequest) -> AskResponse:
    if retriever is None:
        raise HTTPException(status_code=503, detail="Retriever is not ready")
    results = retriever.search(request.question, request.top_k)
    answer = await answer_with_optional_llm(request.question, results)
    return AskResponse(answer=answer, sources=[to_result(doc, score) for doc, score in results])
