from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import get_bearer_token, validate_token_session
from ..config import DEFAULT_TOP_K, MAX_TOP_K
from ..corpus import Document
from ..db import get_session
from ..qa import answer_with_optional_llm
from ..schemas import AskRequest, AskResponse, SearchResult
from ..vector_retriever import VectorRetriever

router = APIRouter(prefix="/api", tags=["rag"])

documents: list[Document] = []
retriever: VectorRetriever | None = None


def configure_rag(loaded_documents: list[Document], loaded_retriever: VectorRetriever) -> None:
    global documents, retriever
    documents = loaded_documents
    retriever = loaded_retriever


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


async def require_rag_session(
    session: Annotated[AsyncSession, Depends(get_session)],
    token_value: Annotated[str, Depends(get_bearer_token)],
    x_session_id: Annotated[str | None, Header()] = None,
) -> None:
    await validate_token_session(session, token_value, x_session_id)


@router.get("/search", response_model=list[SearchResult])
async def search(
    _: Annotated[None, Depends(require_rag_session)],
    q: Annotated[str, Query(min_length=1, max_length=1000)],
    top_k: Annotated[int, Query(ge=1, le=MAX_TOP_K)] = DEFAULT_TOP_K,
) -> list[SearchResult]:
    if retriever is None:
        raise HTTPException(status_code=503, detail="Retriever is not ready")
    return [to_result(doc, score) for doc, score in retriever.search(q, top_k)]


@router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest, _: Annotated[None, Depends(require_rag_session)]) -> AskResponse:
    if retriever is None:
        raise HTTPException(status_code=503, detail="Retriever is not ready")
    results = retriever.search(request.question, request.top_k)
    answer = await answer_with_optional_llm(request.question, results)
    return AskResponse(answer=answer, sources=[to_result(doc, score) for doc, score in results])
