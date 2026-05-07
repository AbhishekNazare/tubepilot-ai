import { useMemo, useState } from "react";
import { DemoVideo, RiskLevel, demoVideos } from "../demoData";
import { MetricCard } from "../components/MetricCard";
import { RiskTable } from "../components/RiskTable";

const riskOptions: Array<"all" | RiskLevel> = ["all", "high", "medium", "low"];

export function VideoRisk() {
  const [filter, setFilter] = useState<"all" | RiskLevel>("all");
  const [selectedVideoId, setSelectedVideoId] = useState(demoVideos[0].id);
  const selected = demoVideos.find((video) => video.id === selectedVideoId) ?? demoVideos[0];
  const filtered = useMemo(
    () => (filter === "all" ? demoVideos : demoVideos.filter((video) => video.riskLevel === filter)),
    [filter],
  );

  return (
    <div className="page-stack">
      <section className="insight-panel">
        <div className="panel-heading">
          <div>
            <span className="eyebrow">Selected Video</span>
            <h3>{selected.title}</h3>
          </div>
        </div>
        <div className="metric-grid">
          <MetricCard label="Risk score" value={`${Math.round(selected.riskScore * 100)}`} tone="watch" />
          <MetricCard label="CTR" value={`${selected.ctr.toFixed(1)}%`} tone={selected.ctr >= 7 ? "good" : "watch"} />
          <MetricCard label="Retention" value={`${selected.retention.toFixed(1)}%`} tone={selected.retention >= 45 ? "good" : "watch"} />
          <MetricCard label="Views" value={new Intl.NumberFormat("en-US").format(selected.views)} />
        </div>
        <div className="recommendation">
          <span>Recommended action</span>
          <p>{selected.action}</p>
        </div>
      </section>

      <section className="panel video-panel">
        <div className="panel-heading compact">
          <div>
            <span className="eyebrow">Video Risk Dashboard</span>
            <h3>Prioritized Reviews</h3>
          </div>
          <div className="segmented-control">
            {riskOptions.map((option) => (
              <button className={option === filter ? "active" : ""} key={option} onClick={() => setFilter(option)}>
                {option}
              </button>
            ))}
          </div>
        </div>
        <RiskTable videos={filtered as DemoVideo[]} selectedVideoId={selectedVideoId} onSelectVideo={setSelectedVideoId} />
      </section>
    </div>
  );
}

