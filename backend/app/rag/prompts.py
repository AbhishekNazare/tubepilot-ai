from app.rag.retrieval import RetrievedChunk


def build_cited_context(chunks: list[RetrievedChunk]) -> str:
    return "\n\n".join(
        f"[{chunk.chunk_id}] {chunk.title}\n{chunk.text}"
        for chunk in chunks
    )

