import { AgentStepTimeline } from "../components/AgentStepTimeline";

const demoSteps = [
  { step: 1, tool: "get_recent_videos", summary: "Fetch latest uploads for the selected channel." },
  { step: 2, tool: "get_video_metrics", summary: "Load CTR, retention, views, and subscriber movement." },
  { step: 3, tool: "predict_video_risk", summary: "Run the baseline ML underperformance model." },
  { step: 4, tool: "search_creator_docs", summary: "Retrieve title, thumbnail, and retention guidance." },
  { step: 5, tool: "generate_action_plan", summary: "Return recommendations with citations and traceable steps." },
];

export function AgentTimeline() {
  return (
    <section className="panel timeline-panel">
      <div className="panel-heading compact">
        <div>
          <span className="eyebrow">Transparent Workflow</span>
          <h3>Agent Timeline</h3>
        </div>
      </div>
      <AgentStepTimeline steps={demoSteps} />
    </section>
  );
}

