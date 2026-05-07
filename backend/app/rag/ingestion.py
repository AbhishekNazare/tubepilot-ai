from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import uuid5, NAMESPACE_URL

from sqlalchemy.orm import Session

from app.db.models import Document, DocumentChunk
from app.rag.chunking import chunk_text

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DOCS_DIR = PROJECT_ROOT / "docs"


@dataclass(frozen=True)
class IngestedDocument:
    document_id: str
    title: str
    chunks_created: int


def title_from_markdown(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return fallback


def ingest_markdown_document(session: Session, path: Path) -> IngestedDocument:
    resolved_path = path if path.is_absolute() else PROJECT_ROOT / path
    text = resolved_path.read_text(encoding="utf-8")
    title = title_from_markdown(text, resolved_path.stem.replace("_", " ").title())
    document_id = f"doc_{uuid5(NAMESPACE_URL, str(resolved_path)).hex[:12]}"

    session.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).delete()
    session.query(Document).filter(Document.document_id == document_id).delete()
    session.add(
        Document(
            document_id=document_id,
            title=title,
            source_type="markdown",
            ingested_at=datetime.utcnow(),
        )
    )

    chunks = chunk_text(text)
    for chunk in chunks:
        chunk_id = f"{document_id}_chunk_{chunk.chunk_index:03d}"
        session.add(
            DocumentChunk(
                chunk_id=chunk_id,
                document_id=document_id,
                chunk_index=chunk.chunk_index,
                text=chunk.text,
                qdrant_point_id=chunk_id,
            )
        )
    session.commit()
    return IngestedDocument(document_id=document_id, title=title, chunks_created=len(chunks))


def ingest_default_documents(session: Session, docs_dir: Path = DOCS_DIR) -> list[IngestedDocument]:
    source_paths = sorted(
        path
        for path in docs_dir.glob("*.md")
        if path.name
        in {
            "youtube_monetization.md",
            "creator_best_practices.md",
            "retention_tips.md",
            "title_thumbnail_strategy.md",
            "upload_consistency.md",
        }
    )
    return [ingest_markdown_document(session, path) for path in source_paths]

