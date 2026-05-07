from dataclasses import dataclass
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Document, DocumentChunk
from app.rag.embeddings import HashEmbeddingModel, cosine_similarity


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: str
    document_id: str
    title: str
    text: str
    score: float


def search_creator_docs(
    session: Session,
    query: str,
    top_k: int = 4,
    embedding_model: Optional[HashEmbeddingModel] = None,
) -> list[RetrievedChunk]:
    model = embedding_model or HashEmbeddingModel()
    query_vector = model.embed(query)

    rows = session.execute(
        select(DocumentChunk, Document)
        .join(Document, Document.document_id == DocumentChunk.document_id)
        .order_by(Document.title, DocumentChunk.chunk_index)
    ).all()

    ranked = []
    for chunk, document in rows:
        score = cosine_similarity(query_vector, model.embed(chunk.text))
        ranked.append(
            RetrievedChunk(
                chunk_id=chunk.chunk_id,
                document_id=document.document_id,
                title=document.title,
                text=chunk.text,
                score=round(score, 4),
            )
        )

    return sorted(ranked, key=lambda item: item.score, reverse=True)[:top_k]
