import json
from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.agents.schemas import AgentStepResult, ChatResponse, Citation
from app.agents.tools import (
    generate_action_plan,
    get_channel_metrics,
    get_recent_videos,
    get_video_metrics,
    predict_video_underperformance,
    search_creator_guidance,
)
from app.db.models import AgentRun, AgentStep


class CreatorAgent:
    def run(self, session: Session, channel_id: str, query: str) -> ChatResponse:
        run_id = f"run_{uuid4().hex[:12]}"
        steps: list[AgentStepResult] = []

        recent_videos = get_recent_videos(session, channel_id, limit=3)
        if not recent_videos:
            raise ValueError(f"No videos found for channel_id: {channel_id}")
        latest_video = recent_videos[0]
        steps.append(
            self._step(
                1,
                "get_recent_videos",
                {"channel_id": channel_id, "limit": 3},
                f"Fetched {len(recent_videos)} recent videos; latest is {latest_video.video_id}.",
            )
        )

        video_metrics = get_video_metrics(session, latest_video.video_id)
        steps.append(
            self._step(
                2,
                "get_video_metrics",
                {"video_id": latest_video.video_id},
                (
                    f"Loaded {video_metrics.views} views, {video_metrics.ctr:.1f}% CTR, "
                    f"and {video_metrics.retention_percentage:.1f}% retention."
                ),
            )
        )

        channel_metrics = get_channel_metrics(session, channel_id)
        steps.append(
            self._step(
                3,
                "get_channel_metrics",
                {"channel_id": channel_id},
                (
                    f"Loaded channel baseline: {channel_metrics.avg_ctr:.1f}% CTR and "
                    f"{channel_metrics.avg_retention:.1f}% retention."
                ),
            )
        )

        prediction = predict_video_underperformance(session, latest_video.video_id)
        steps.append(
            self._step(
                4,
                "predict_video_risk",
                {"video_id": latest_video.video_id},
                f"Computed {prediction.risk_level} risk score of {prediction.risk_score:.2f}.",
            )
        )

        rag_query = f"{query} {' '.join(prediction.top_factors)} CTR retention title thumbnail"
        citations = search_creator_guidance(session, rag_query, top_k=3)
        steps.append(
            self._step(
                5,
                "search_creator_docs",
                {"query": rag_query, "top_k": 3},
                f"Retrieved {len(citations)} creator guidance chunks.",
            )
        )

        answer = generate_action_plan(video_metrics, channel_metrics, prediction, citations)
        steps.append(
            self._step(
                6,
                "generate_action_plan",
                {"video_id": latest_video.video_id},
                "Generated cited explanation and next-step action plan.",
            )
        )

        session.add(
            AgentRun(
                run_id=run_id,
                channel_id=channel_id,
                user_query=query,
                final_answer=answer,
                created_at=datetime.utcnow(),
            )
        )
        for step in steps:
            session.add(
                AgentStep(
                    step_id=f"step_{uuid4().hex[:12]}",
                    run_id=run_id,
                    step_order=step.step,
                    tool_name=step.tool,
                    input_payload=json.dumps(step.input_payload),
                    output_summary=step.summary,
                )
            )
        session.commit()

        return ChatResponse(
            run_id=run_id,
            answer=answer,
            video_id=latest_video.video_id,
            risk_score=prediction.risk_score,
            risk_level=prediction.risk_level,
            top_factors=prediction.top_factors,
            citations=[
                Citation(
                    title=chunk.title,
                    chunk_id=chunk.chunk_id,
                    score=chunk.score,
                    text=chunk.text,
                )
                for chunk in citations
            ],
            agent_steps=steps,
        )

    def _step(
        self,
        order: int,
        tool_name: str,
        input_payload: dict[str, object],
        summary: str,
    ) -> AgentStepResult:
        return AgentStepResult(step=order, tool=tool_name, summary=summary, input_payload=input_payload)
