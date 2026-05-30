from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import FRONTEND_DIST_DIR
from .corpus import load_documents
from .db import close_db, init_db
from .routes import admin, auth, rag
from .routes.rag import configure_rag
from .vector_retriever import VectorRetriever


@asynccontextmanager
async def lifespan(app: FastAPI):
    documents = load_documents()
    retriever = VectorRetriever(documents)
    configure_rag(documents, retriever)
    await init_db()
    yield
    await close_db()


app = FastAPI(title="Course RAG", version="0.2.0", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(rag.router)

assets_dir = FRONTEND_DIST_DIR / "assets"
if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")


@app.get("/health")
def health() -> dict[str, int | str]:
    return {"status": "ok", "documents": len(rag.documents)}


@app.get("/{path:path}")
def spa(path: str) -> FileResponse:
    index_path = FRONTEND_DIST_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Frontend build not found")
    return FileResponse(index_path)
