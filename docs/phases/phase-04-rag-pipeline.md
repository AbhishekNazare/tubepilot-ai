# Phase 04: RAG Pipeline

## Branch

```text
phase/04-rag-pipeline
```

## Goal

Index creator strategy documents and retrieve relevant guidance with citations.

## Scope

- Add five to ten markdown creator guidance documents.
- Implement document loading and text cleaning.
- Implement chunking with metadata.
- Generate embeddings and store chunks in Qdrant.
- Add retrieval service.
- Add `POST /documents/ingest` and a retrieval-facing helper.

## Suggested Commits

```text
add creator strategy source documents
implement document chunking pipeline
index document chunks in qdrant
add creator docs retrieval service
test rag retrieval citations
```

## Files To Add Or Update

```text
docs/youtube_monetization.md
docs/creator_best_practices.md
docs/retention_tips.md
docs/title_thumbnail_strategy.md
docs/upload_consistency.md
backend/app/rag/ingestion.py
backend/app/rag/chunking.py
backend/app/rag/embeddings.py
backend/app/rag/retrieval.py
backend/app/rag/prompts.py
backend/app/api/documents.py
backend/tests/test_rag.py
```

## Acceptance Criteria

- Documents can be ingested repeatedly without duplicate confusion.
- Retrieval returns top-k chunks with title, chunk id, and source metadata.
- Answers can include citations from retrieved chunks.
- Tests validate retrieval for known questions.

## Verification

```bash
docker compose up -d qdrant
cd backend && pytest tests/test_rag.py
```

## Push Plan

```bash
git switch main
git pull
git switch -c phase/04-rag-pipeline
git push -u origin phase/04-rag-pipeline
```

