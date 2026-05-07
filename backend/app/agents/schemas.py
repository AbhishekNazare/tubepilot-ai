from pydantic import BaseModel, Field


class Citation(BaseModel):
    title: str
    chunk_id: str
    score: float
    text: str


class AgentStepResult(BaseModel):
    step: int
    tool: str
    summary: str
    input_payload: dict[str, object] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    run_id: str
    answer: str
    video_id: str
    risk_score: float
    risk_level: str
    top_factors: list[str]
    citations: list[Citation]
    agent_steps: list[AgentStepResult]
