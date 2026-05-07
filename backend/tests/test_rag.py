from pathlib import Path

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from app.db.models import Document, DocumentChunk
from app.db.seed import reset_database
from app.rag.chunking import chunk_text, clean_text
from app.rag.ingestion import ingest_default_documents, ingest_markdown_document
from app.rag.prompts import build_cited_context
from app.rag.retrieval import search_creator_docs


def test_chunk_text_creates_overlapping_chunks() -> None:
    text = " ".join(f"word{i}" for i in range(30))

    chunks = chunk_text(text, max_words=12, overlap_words=3)

    assert len(chunks) == 3
    assert chunks[0].text.split()[-3:] == chunks[1].text.split()[:3]
    assert clean_text("A\n\n\nB") == "A\n\nB"


def test_ingest_default_documents_and_search_relevant_chunks() -> None:
    engine = create_engine("sqlite:///:memory:")
    reset_database(engine)

    with Session(engine) as session:
        results = ingest_default_documents(session)
        document_count = session.scalar(select(func.count(Document.document_id)))
        chunk_count = session.scalar(select(func.count(DocumentChunk.chunk_id)))
        retrieved = search_creator_docs(session, "low CTR thumbnail title retention", top_k=3)

    assert len(results) == 5
    assert document_count == 5
    assert chunk_count and chunk_count >= 5
    assert len(retrieved) == 3
    assert any("Thumbnail" in chunk.title or "Retention" in chunk.title for chunk in retrieved)


def test_ingest_single_document_is_idempotent() -> None:
    engine = create_engine("sqlite:///:memory:")
    reset_database(engine)

    with Session(engine) as session:
        first = ingest_markdown_document(session, Path("docs/retention_tips.md"))
        second = ingest_markdown_document(session, Path("docs/retention_tips.md"))
        document_count = session.scalar(select(func.count(Document.document_id)))
        chunk_count = session.scalar(select(func.count(DocumentChunk.chunk_id)))
        retrieved = search_creator_docs(session, "first thirty seconds retention drop", top_k=1)
        context = build_cited_context(retrieved)

    assert first.document_id == second.document_id
    assert document_count == 1
    assert chunk_count == second.chunks_created
    assert "Audience Retention" in context
    assert retrieved[0].chunk_id in context

