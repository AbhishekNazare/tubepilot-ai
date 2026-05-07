import { FormEvent, useState } from "react";
import { Bot, Send, Sparkles } from "lucide-react";
import { ChatResponse, askCreatorAgent } from "../api/client";
import { AgentStepTimeline } from "./AgentStepTimeline";
import { CitationCard } from "./CitationCard";

const fallback: ChatResponse = {
  run_id: "demo_run",
  video_id: "video_105",
  risk_score: 0.24,
  risk_level: "low",
  top_factors: ["healthy_metric_profile"],
  answer:
    "The latest video is currently low risk. CTR and retention are above the recent channel baseline, so the next action is to monitor the upload window and reuse the title structure for the next related topic.",
  citations: [
    {
      title: "Title And Thumbnail Strategy",
      chunk_id: "demo_title_thumbnail",
      score: 0.86,
      text: "Good titles create a specific reason to click and should not overpromise beyond what the first minute proves.",
    },
  ],
  agent_steps: [
    { step: 1, tool: "get_recent_videos", summary: "Fetched latest uploads for channel_001." },
    { step: 2, tool: "get_video_metrics", summary: "Loaded CTR, retention, views, and subscriber movement." },
    { step: 3, tool: "predict_video_risk", summary: "Estimated a low risk score from healthy engagement." },
    { step: 4, tool: "search_creator_docs", summary: "Retrieved title and retention guidance." },
  ],
};

export function ChatPanel() {
  const [query, setQuery] = useState("Why did my latest video underperform?");
  const [response, setResponse] = useState<ChatResponse>(fallback);
  const [status, setStatus] = useState<"idle" | "loading" | "error">("idle");
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setStatus("loading");
    setError(null);
    try {
      setResponse(await askCreatorAgent("channel_001", query));
      setStatus("idle");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to reach the backend");
      setStatus("error");
      setResponse(fallback);
    }
  }

  return (
    <div className="chat-layout">
      <section className="panel chat-panel">
        <div className="panel-heading compact">
          <div>
            <span className="eyebrow">Ask AI</span>
            <h3>Creator Agent</h3>
          </div>
          <Bot size={20} aria-hidden="true" />
        </div>

        <form className="chat-form" onSubmit={handleSubmit}>
          <textarea
            aria-label="Creator question"
            onChange={(event) => setQuery(event.target.value)}
            value={query}
          />
          <button disabled={status === "loading"} type="submit">
            <Send size={16} aria-hidden="true" />
            {status === "loading" ? "Running" : "Ask"}
          </button>
        </form>

        {error ? <div className="notice">Showing demo response. Backend said: {error}</div> : null}

        <div className="answer-card">
          <div>
            <Sparkles size={18} aria-hidden="true" />
            <span>Answer</span>
          </div>
          <p>{response.answer}</p>
        </div>
      </section>

      <section className="panel">
        <div className="panel-heading compact">
          <div>
            <span className="eyebrow">Evidence</span>
            <h3>Citations</h3>
          </div>
        </div>
        <div className="citation-list">
          {response.citations.map((citation) => (
            <CitationCard citation={citation} key={citation.chunk_id} />
          ))}
        </div>
      </section>

      <section className="panel timeline-panel wide">
        <div className="panel-heading compact">
          <div>
            <span className="eyebrow">Execution</span>
            <h3>Agent Timeline</h3>
          </div>
        </div>
        <AgentStepTimeline steps={response.agent_steps} />
      </section>
    </div>
  );
}

