from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    chunk_index: int
    text: str


def clean_text(text: str) -> str:
    lines = [line.strip() for line in text.replace("\r\n", "\n").split("\n")]
    compact_lines: list[str] = []
    previous_blank = False
    for line in lines:
        blank = not line
        if blank and previous_blank:
            continue
        compact_lines.append(line)
        previous_blank = blank
    return "\n".join(compact_lines).strip()


def chunk_text(text: str, max_words: int = 120, overlap_words: int = 24) -> list[TextChunk]:
    words = clean_text(text).split()
    if not words:
        return []
    if max_words <= overlap_words:
        raise ValueError("max_words must be greater than overlap_words")

    chunks: list[TextChunk] = []
    start = 0
    while start < len(words):
        end = min(start + max_words, len(words))
        chunks.append(TextChunk(chunk_index=len(chunks), text=" ".join(words[start:end])))
        if end == len(words):
            break
        start = end - overlap_words
    return chunks

