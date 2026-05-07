import { ChevronRight } from "lucide-react";
import { DemoVideo, RiskLevel } from "../demoData";

export function RiskBadge({ level }: { level: RiskLevel }) {
  return <span className={`risk-badge ${level}`}>{level}</span>;
}

export function RiskTable({
  videos,
  selectedVideoId,
  onSelectVideo,
}: {
  videos: DemoVideo[];
  selectedVideoId: string;
  onSelectVideo: (videoId: string) => void;
}) {
  return (
    <div className="video-list">
      {videos.map((video) => (
        <button
          className={`video-row ${video.id === selectedVideoId ? "active" : ""}`}
          key={video.id}
          onClick={() => onSelectVideo(video.id)}
          type="button"
        >
          <div>
            <strong>{video.title}</strong>
            <span>
              {video.channel} · {video.publishedAt} · {video.topFactors.join(", ")}
            </span>
          </div>
          <RiskBadge level={video.riskLevel} />
          <span className="score">{Math.round(video.riskScore * 100)}</span>
          <ChevronRight size={18} aria-hidden="true" />
        </button>
      ))}
    </div>
  );
}

