from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.rag.ingestion import ingest_default_documents, ingest_markdown_document
from app.rag.retrieval import search_creator_docs

router = APIRouter(prefix="/documents", tags=["documents"])


class DocumentIngestRequest(BaseModel):
    path: Optional[str] = Field(default=None, examples=["docs/creator_best_practices.md"])


class DocumentIngestResponse(BaseModel):
    documents_ingested: int
    chunks_created: int
    document_ids: list[str]
    status: str


class DocumentSearchRequest(BaseModel):
    query: str = Field(examples=["How should I fix low CTR and retention?"])
    top_k: int = Field(default=4, ge=1, le=10)


class CitationResponse(BaseModel):
    title: str
    chunk_id: str
    score: float
    text: str


class DocumentSearchResponse(BaseModel):
    query: str
    citations: list[CitationResponse]


@router.post("/ingest", response_model=DocumentIngestResponse)
def ingest_documents(
    request: DocumentIngestRequest,
    db: Session = Depends(get_db),
) -> DocumentIngestResponse:
    results = (
        [ingest_markdown_document(db, Path(request.path))]
        if request.path
        else ingest_default_documents(db)
    )
    return DocumentIngestResponse(
        documents_ingested=len(results),
        chunks_created=sum(result.chunks_created for result in results),
        document_ids=[result.document_id for result in results],
        status="indexed",
    )


@router.post("/search", response_model=DocumentSearchResponse)
def search_documents(
    request: DocumentSearchRequest,
    db: Session = Depends(get_db),
) -> DocumentSearchResponse:
    chunks = search_creator_docs(db, request.query, request.top_k)
    return DocumentSearchResponse(
        query=request.query,
        citations=[
            CitationResponse(
                title=chunk.title,
                chunk_id=chunk.chunk_id,
                score=chunk.score,
                text=chunk.text,
            )
            for chunk in chunks
        ],
    )
