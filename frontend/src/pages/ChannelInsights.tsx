import { BarChart3 } from "lucide-react";
import { demoVideos, weeklyTrend } from "../demoData";
import { MetricCard } from "../components/MetricCard";

type Metric = "views" | "ctr" | "retention";

function TrendBars({ metric }: { metric: Metric }) {
  const max = Math.max(...weeklyTrend.map((item) => item[metric]));
  return (
    <div className="trend-bars">
      {weeklyTrend.map((item) => (
        <div className="trend-column" key={item.label}>
          <div className="bar-track">
            <div className={`bar-fill ${metric}`} style={{ height: `${Math.max(12, (item[metric] / max) * 100)}%` }} />
          </div>
          <span>{item.label}</span>
        </div>
      ))}
    </div>
  );
}

export function ChannelInsights() {
  const totalViews = demoVideos.reduce((sum, video) => sum + video.views, 0);
  const avgCtr = demoVideos.reduce((sum, video) => sum + video.ctr, 0) / demoVideos.length;
  const avgRetention = demoVideos.reduce((sum, video) => sum + video.retention, 0) / demoVideos.length;

  return (
    <div className="page-stack">
      <section className="summary-panel insight-summary">
        <MetricCard label="Total demo views" value={new Intl.NumberFormat("en-US").format(totalViews)} />
        <MetricCard label="Average CTR" value={`${avgCtr.toFixed(1)}%`} tone="good" />
        <MetricCard label="Average retention" value={`${avgRetention.toFixed(1)}%`} tone="watch" />
      </section>

      <section className="panel trend-panel">
        <div className="panel-heading compact">
          <div>
            <span className="eyebrow">Channel Trend</span>
            <h3>Weekly Movement</h3>
          </div>
          <BarChart3 size={20} aria-hidden="true" />
        </div>
        <TrendBars metric="views" />
      </section>
    </div>
  );
}

