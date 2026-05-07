import { useState } from "react";
import { BarChart3, Bot, Clock3, Gauge, Sparkles } from "lucide-react";
import { AskAI } from "./pages/AskAI";
import { AgentTimeline } from "./pages/AgentTimeline";
import { ChannelInsights } from "./pages/ChannelInsights";
import { VideoRisk } from "./pages/VideoRisk";
import "./App.css";

const pages = [
  { id: "ask", label: "Ask AI", icon: Bot, eyebrow: "Agent Console", title: "Ask TubePilot AI" },
  { id: "risk", label: "Risk", icon: Gauge, eyebrow: "Prediction", title: "Video Risk Dashboard" },
  { id: "insights", label: "Insights", icon: BarChart3, eyebrow: "Analytics", title: "Channel Insights" },
  { id: "timeline", label: "Timeline", icon: Clock3, eyebrow: "Trace", title: "Agent Timeline" },
] as const;

type PageId = (typeof pages)[number]["id"];

function renderPage(page: PageId) {
  if (page === "risk") return <VideoRisk />;
  if (page === "insights") return <ChannelInsights />;
  if (page === "timeline") return <AgentTimeline />;
  return <AskAI />;
}

function App() {
  const [activePage, setActivePage] = useState<PageId>("ask");
  const page = pages.find((item) => item.id === activePage) ?? pages[0];

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
          {pages.map((item) => {
            const Icon = item.icon;
            return (
              <button
                className={item.id === activePage ? "nav-item active" : "nav-item"}
                key={item.id}
                onClick={() => setActivePage(item.id)}
                type="button"
              >
                <Icon size={18} aria-hidden="true" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="sidebar-card">
          <span>MVP Dataset</span>
          <strong>2 channels · 10 videos</strong>
          <p>Seed-ready analytics, RAG citations, ML risk scores, and persisted agent traces.</p>
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <span className="eyebrow">{page.eyebrow}</span>
            <h2>{page.title}</h2>
          </div>
          <div className="status-card">
            <span>Phase 06</span>
            <strong>Demo-ready dashboard</strong>
          </div>
        </header>
        {renderPage(activePage)}
      </main>
    </div>
  );
}

export default App;

