import { useMemo, useState } from "react";
import {
  Activity,
  BarChart3,
  Bot,
  CheckCircle2,
  ChevronRight,
  Clock3,
  Database,
  Gauge,
  LineChart,
  Search,
  Sparkles,
  TrendingDown,
  TrendingUp,
} from "lucide-react";
import { DemoVideo, RiskLevel, demoVideos, weeklyTrend } from "./demoData";
import "./App.css";

const navItems = [
  { label: "Ask AI", icon: Bot },
  { label: "Risk", icon: Gauge },
  { label: "Insights", icon: BarChart3 },
  { label: "Timeline", icon: Clock3 },
];

const riskOptions: Array<"all" | RiskLevel> = ["all", "high", "medium", "low"];
const metricOptions = ["views", "ctr", "retention"] as const;
type MetricOption = (typeof metricOptions)[number];

function formatNumber(value: number) {
  return new Intl.NumberFormat("en-US", { notation: "compact" }).format(value);
}

function riskLabel(level: RiskLevel) {
  return level.charAt(0).toUpperCase() + level.slice(1);
}

function RiskBadge({ level }: { level: RiskLevel }) {
  return <span className={`risk-badge ${level}`}>{riskLabel(level)}</span>;
}

function MetricTile({
  label,
  value,
  tone,
}: {
  label: string;
  value: string;
  tone: "good" | "watch" | "neutral";
}) {
  return (
    <div className={`metric-tile ${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function TrendBars({ metric }: { metric: MetricOption }) {
  const max = Math.max(...weeklyTrend.map((item) => item[metric]));

  return (
    <div className="trend-bars" aria-label={`${metric} trend`}>
      {weeklyTrend.map((item) => (
        <div className="trend-column" key={item.label}>
          <div className="bar-track">
            <div
              className={`bar-fill ${metric}`}
              style={{ height: `${Math.max(12, (item[metric] / max) * 100)}%` }}
            />
          </div>
          <span>{item.label}</span>
        </div>
      ))}
    </div>
  );
}

function VideoRow({
  video,
  active,
  onSelect,
}: {
  video: DemoVideo;
  active: boolean;
  onSelect: () => void;
}) {
  return (
    <button className={`video-row ${active ? "active" : ""}`} onClick={onSelect} type="button">
      <div>
        <strong>{video.title}</strong>
        <span>
          {video.channel} · {video.publishedAt}
        </span>
      </div>
      <RiskBadge level={video.riskLevel} />
      <span className="score">{Math.round(video.riskScore * 100)}</span>
      <ChevronRight size={18} aria-hidden="true" />
    </button>
  );
}

function App() {
  const [selectedVideoId, setSelectedVideoId] = useState(demoVideos[0].id);
  const [riskFilter, setRiskFilter] = useState<"all" | RiskLevel>("all");
  const [metric, setMetric] = useState<MetricOption>("views");
  const [query, setQuery] = useState("Why did my latest video underperform?");

  const selectedVideo = demoVideos.find((video) => video.id === selectedVideoId) ?? demoVideos[0];
  const filteredVideos = useMemo(
    () =>
      riskFilter === "all"
        ? demoVideos
        : demoVideos.filter((video) => video.riskLevel === riskFilter),
    [riskFilter],
  );
  const highRiskCount = demoVideos.filter((video) => video.riskLevel === "high").length;
  const avgCtr = demoVideos.reduce((sum, video) => sum + video.ctr, 0) / demoVideos.length;
  const avgRetention =
    demoVideos.reduce((sum, video) => sum + video.retention, 0) / demoVideos.length;

  const agentSteps = [
    {
      icon: Database,
      title: "Loaded synthetic metrics",
      copy: `${selectedVideo.views.toLocaleString()} views and ${selectedVideo.impressions.toLocaleString()} impressions.`,
    },
    {
      icon: TrendingDown,
      title: "Compared against baseline",
      copy: `${selectedVideo.ctr.toFixed(1)}% CTR and ${selectedVideo.retention.toFixed(1)}% retention.`,
    },
    {
      icon: Gauge,
      title: "Estimated risk",
      copy: `${Math.round(selectedVideo.riskScore * 100)} risk score from ${selectedVideo.topFactors.join(", ")}.`,
    },
    {
      icon: Sparkles,
      title: "Prepared next action",
      copy: selectedVideo.action,
    },
  ];

  return (
    <div className="app-shell">
      <aside className="sidebar" aria-label="Primary navigation">
        <div className="brand">
          <div className="brand-mark">
            <Sparkles size={20} aria-hidden="true" />
          </div>
          <div>
            <h1>TubePilot AI</h1>
            <p>Creator Copilot</p>
          </div>
        </div>

        <nav className="nav-list">
          {navItems.map((item, index) => {
            const Icon = item.icon;
            return (
              <button className={index === 0 ? "nav-item active" : "nav-item"} key={item.label}>
                <Icon size={18} aria-hidden="true" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="sidebar-card">
          <span>Dataset</span>
          <strong>2 channels · 10 videos</strong>
          <p>Seed-ready analytics with CTR, retention, views, and subscriber movement.</p>
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <span className="eyebrow">Phase 02</span>
            <h2>Creator Performance Command Center</h2>
          </div>
          <div className="search-shell">
            <Search size={18} aria-hidden="true" />
            <input
              aria-label="Ask TubePilot AI"
              onChange={(event) => setQuery(event.target.value)}
              value={query}
            />
          </div>
        </header>

        <section className="hero-grid">
          <div className="insight-panel">
            <div className="panel-heading">
              <div>
                <span className="eyebrow">Selected Analysis</span>
                <h3>{selectedVideo.title}</h3>
              </div>
              <RiskBadge level={selectedVideo.riskLevel} />
            </div>

            <div className="metric-grid">
              <MetricTile label="Risk score" value={`${Math.round(selectedVideo.riskScore * 100)}`} tone="watch" />
              <MetricTile label="CTR" value={`${selectedVideo.ctr.toFixed(1)}%`} tone={selectedVideo.ctr >= 7 ? "good" : "watch"} />
              <MetricTile label="Retention" value={`${selectedVideo.retention.toFixed(1)}%`} tone={selectedVideo.retention >= 45 ? "good" : "watch"} />
              <MetricTile label="Views" value={formatNumber(selectedVideo.views)} tone="neutral" />
            </div>

            <div className="recommendation">
              <div>
                <Activity size={18} aria-hidden="true" />
                <span>Recommended action</span>
              </div>
              <p>{selectedVideo.action}</p>
            </div>
          </div>

          <div className="summary-panel">
            <div className="summary-stat">
              <span>High risk videos</span>
              <strong>{highRiskCount}</strong>
            </div>
            <div className="summary-stat">
              <span>Average CTR</span>
              <strong>{avgCtr.toFixed(1)}%</strong>
            </div>
            <div className="summary-stat">
              <span>Average retention</span>
              <strong>{avgRetention.toFixed(1)}%</strong>
            </div>
            <div className="delta-card">
              <TrendingUp size={18} aria-hidden="true" />
              <span>Latest low-risk upload is outperforming the prior channel baseline.</span>
            </div>
          </div>
        </section>

        <section className="workspace-grid">
          <div className="panel video-panel">
            <div className="panel-heading compact">
              <div>
                <span className="eyebrow">Video Risk Queue</span>
                <h3>Prioritized Reviews</h3>
              </div>
              <div className="segmented-control" aria-label="Risk filter">
                {riskOptions.map((option) => (
                  <button
                    className={option === riskFilter ? "active" : ""}
                    key={option}
                    onClick={() => setRiskFilter(option)}
                    type="button"
                  >
                    {option === "all" ? "All" : riskLabel(option)}
                  </button>
                ))}
              </div>
            </div>

            <div className="video-list">
              {filteredVideos.map((video) => (
                <VideoRow
                  active={video.id === selectedVideo.id}
                  key={video.id}
                  onSelect={() => setSelectedVideoId(video.id)}
                  video={video}
                />
              ))}
            </div>
          </div>

          <div className="panel trend-panel">
            <div className="panel-heading compact">
              <div>
                <span className="eyebrow">Channel Trend</span>
                <h3>Weekly Movement</h3>
              </div>
              <LineChart size={20} aria-hidden="true" />
            </div>

            <div className="metric-tabs" aria-label="Trend metric">
              {metricOptions.map((option) => (
                <button
                  className={option === metric ? "active" : ""}
                  key={option}
                  onClick={() => setMetric(option)}
                  type="button"
                >
                  {option}
                </button>
              ))}
            </div>

            <TrendBars metric={metric} />
          </div>
        </section>

        <section className="panel timeline-panel">
          <div className="panel-heading compact">
            <div>
              <span className="eyebrow">Transparent Workflow</span>
              <h3>Agent Timeline Preview</h3>
            </div>
            <CheckCircle2 size={20} aria-hidden="true" />
          </div>

          <div className="timeline">
            {agentSteps.map((step, index) => {
              const Icon = step.icon;
              return (
                <div className="timeline-step" key={step.title}>
                  <span className="step-index">{index + 1}</span>
                  <div className="step-icon">
                    <Icon size={18} aria-hidden="true" />
                  </div>
                  <div>
                    <strong>{step.title}</strong>
                    <p>{step.copy}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;

