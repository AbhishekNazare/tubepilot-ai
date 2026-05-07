export type Citation = {
  title: string;
  chunk_id: string;
  score: number;
  text: string;
};

export type AgentStep = {
  step: number;
  tool: string;
  summary: string;
  input_payload?: Record<string, unknown>;
};

export type ChatResponse = {
  run_id: string;
  answer: string;
  video_id: string;
  risk_score: number;
  risk_level: string;
  top_factors: string[];
  citations: Citation[];
  agent_steps: AgentStep[];
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string, options: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? `Request failed with ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function askCreatorAgent(channelId: string, query: string): Promise<ChatResponse> {
  return request<ChatResponse>("/chat", {
    method: "POST",
    body: JSON.stringify({ channel_id: channelId, query }),
  });
}

