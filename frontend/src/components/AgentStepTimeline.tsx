import { CheckCircle2 } from "lucide-react";
import { AgentStep } from "../api/client";

export function AgentStepTimeline({ steps }: { steps: AgentStep[] }) {
  return (
    <div className="timeline">
      {steps.map((step) => (
        <div className="timeline-step" key={`${step.step}-${step.tool}`}>
          <span className="step-index">{step.step}</span>
          <div className="step-icon">
            <CheckCircle2 size={18} aria-hidden="true" />
          </div>
          <div>
            <strong>{step.tool}</strong>
            <p>{step.summary}</p>
          </div>
        </div>
      ))}
    </div>
  );
}

