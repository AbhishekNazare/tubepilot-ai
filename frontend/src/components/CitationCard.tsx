import { Citation } from "../api/client";

export function CitationCard({ citation }: { citation: Citation }) {
  return (
    <article className="citation-card">
      <div>
        <strong>{citation.title}</strong>
        <span>{citation.chunk_id}</span>
      </div>
      <p>{citation.text}</p>
      <small>Relevance {(citation.score * 100).toFixed(0)}%</small>
    </article>
  );
}

