import { BarChart3, Bot, Clock3, FileSearch, Gauge } from "lucide-react";
import "./App.css";

const navItems = [
  { label: "Ask AI", icon: Bot, active: true },
  { label: "Video Risk", icon: Gauge, active: false },
  { label: "Insights", icon: BarChart3, active: false },
  { label: "Timeline", icon: Clock3, active: false },
  { label: "Documents", icon: FileSearch, active: false },
];

const timeline = [
  ["Fetch metrics", "Pull latest channel and video analytics from the API."],
  ["Predict risk", "Run the baseline video underperformance model."],
  ["Retrieve docs", "Search creator strategy and YouTube policy notes."],
  ["Generate plan", "Return cited recommendations and next actions."],
];

function App() {
  return (
    <div className="app-shell">
      <aside className="sidebar" aria-label="Primary navigation">
        <div className="brand">
          <h1 className="brand-title">TubePilot AI</h1>
          <p className="brand-subtitle">YouTube Creator Copilot</p>
        </div>

        <nav className="nav-list">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                className={item.active ? "nav-item active" : "nav-item"}
                key={item.label}
                type="button"
              >
                <Icon size={18} aria-hidden="true" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </aside>

      <main className="main-panel">
        <header className="page-header">
          <div>
            <h1>Ask AI</h1>
            <p>
              Analyze creator performance by combining channel metrics, risk
              prediction, retrieved strategy guidance, and an auditable agent
              timeline.
            </p>
          </div>
          <span className="status-pill">API ready: /health</span>
        </header>

        <section className="content-grid">
          <div className="panel">
            <div className="panel-header">
              <h2>Creator Question</h2>
            </div>
            <div className="panel-body chat-box">
              <div className="message user">
                Why did my latest video underperform?
              </div>
              <div className="message assistant">
                The full agent workflow will appear here in later phases. This
                shell establishes the dashboard layout and API connection target
                for the MVP.
              </div>
            </div>
          </div>

          <aside className="panel">
            <div className="panel-header">
              <h2>Phase 01 Baseline</h2>
            </div>
            <div className="panel-body">
              <div className="metric-grid">
                <div className="metric">
                  <div className="metric-label">Backend</div>
                  <div className="metric-value">FastAPI</div>
                </div>
                <div className="metric">
                  <div className="metric-label">Frontend</div>
                  <div className="metric-value">React</div>
                </div>
                <div className="metric">
                  <div className="metric-label">Infra</div>
                  <div className="metric-value">Docker</div>
                </div>
              </div>
            </div>
          </aside>
        </section>

        <section className="panel" style={{ marginTop: 18 }}>
          <div className="panel-header">
            <h2>Planned Agent Timeline</h2>
          </div>
          <div className="panel-body timeline">
            {timeline.map(([title, copy], index) => (
              <div className="timeline-step" key={title}>
                <span className="step-index">{index + 1}</span>
                <div>
                  <p className="step-title">{title}</p>
                  <p className="step-copy">{copy}</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;

