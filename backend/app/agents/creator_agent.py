import json
from datetime import datetime
from enum import Enum
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
from app.rag.retrieval import RetrievedChunk


class QueryIntent(str, Enum):
    PRODUCT_HELP = "product_help"
    CREATOR_GUIDANCE = "creator_guidance"
    VIDEO_ANALYSIS = "video_analysis"


class CreatorAgent:
    def run(self, session: Session, channel_id: str, query: str) -> ChatResponse:
        run_id = f"run_{uuid4().hex[:12]}"
        steps: list[AgentStepResult] = []
        intent = self._classify_intent(query)
        steps.append(
            self._step(
                1,
                "classify_query",
                {"query": query},
                f"Classified request as {intent.value}.",
            )
        )

        if intent == QueryIntent.PRODUCT_HELP:
            return self._run_product_help(session, run_id, channel_id, query, steps)

        if intent == QueryIntent.CREATOR_GUIDANCE:
            return self._run_guidance_search(session, run_id, channel_id, query, steps)

        return self._run_video_analysis(session, run_id, channel_id, query, steps)

    def _run_video_analysis(
        self,
        session: Session,
        run_id: str,
        channel_id: str,
        query: str,
        steps: list[AgentStepResult],
    ) -> ChatResponse:
        recent_videos = get_recent_videos(session, channel_id, limit=3)
        if not recent_videos:
            raise ValueError(f"No videos found for channel_id: {channel_id}")
        latest_video = recent_videos[0]
        steps.append(
            self._step(
                2,
                "get_recent_videos",
                {"channel_id": channel_id, "limit": 3},
                f"Fetched {len(recent_videos)} recent videos; latest is {latest_video.video_id}.",
            )
        )

        video_metrics = get_video_metrics(session, latest_video.video_id)
        steps.append(
            self._step(
                3,
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
                4,
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
                5,
                "predict_video_risk",
                {"video_id": latest_video.video_id},
                f"Computed {prediction.risk_level} risk score of {prediction.risk_score:.2f}.",
            )
        )

        rag_query = f"{query} {' '.join(prediction.top_factors)} CTR retention title thumbnail"
        citations = search_creator_guidance(session, rag_query, top_k=3)
        steps.append(
            self._step(
                6,
                "search_creator_docs",
                {"query": rag_query, "top_k": 3},
                f"Retrieved {len(citations)} creator guidance chunks.",
            )
        )

        answer = generate_action_plan(video_metrics, channel_metrics, prediction, citations)
        steps.append(
            self._step(
                7,
                "generate_action_plan",
                {"video_id": latest_video.video_id},
                "Generated cited explanation and next-step action plan.",
            )
        )

        self._persist_run(session, run_id, channel_id, query, answer, steps)
        return ChatResponse(
            run_id=run_id,
            answer=answer,
            video_id=latest_video.video_id,
            risk_score=prediction.risk_score,
            risk_level=prediction.risk_level,
            top_factors=prediction.top_factors,
            citations=[self._citation(chunk) for chunk in citations],
            agent_steps=steps,
        )

    def _run_product_help(
        self,
        session: Session,
        run_id: str,
        channel_id: str,
        query: str,
        steps: list[AgentStepResult],
    ) -> ChatResponse:
        answer = (
            "TubePilot AI is a creator analytics copilot. This MVP combines synthetic "
            "YouTube-style metrics, a video-risk predictor, a small creator-guidance RAG corpus, "
            "and an auditable agent timeline. Ask performance questions like why the latest video "
            "underperformed, strategy questions like how to improve CTR, or policy-style questions "
            "like what monetization guidance applies. The answer panel shows the result, Evidence "
            "shows retrieved guidance, and Timeline shows which tools ran."
        )
        steps.append(
            self._step(
                2,
                "describe_product",
                {"query": query},
                "Explained the product instead of running video-risk analysis.",
            )
        )
        self._persist_run(session, run_id, channel_id, query, answer, steps)
        return ChatResponse(
            run_id=run_id,
            answer=answer,
            video_id="not_applicable",
            risk_score=0.0,
            risk_level="not_applicable",
            top_factors=[],
            citations=[],
            agent_steps=steps,
        )

    def _run_guidance_search(
        self,
        session: Session,
        run_id: str,
        channel_id: str,
        query: str,
        steps: list[AgentStepResult],
    ) -> ChatResponse:
        citations = search_creator_guidance(session, query, top_k=3)
        steps.append(
            self._step(
                2,
                "search_creator_docs",
                {"query": query, "top_k": 3},
                f"Retrieved {len(citations)} creator guidance chunks.",
            )
        )
        answer = self._guidance_answer(query, citations)
        steps.append(
            self._step(
                3,
                "generate_guidance_answer",
                {"citation_count": len(citations)},
                "Generated a guidance answer from retrieved documents.",
            )
        )
        self._persist_run(session, run_id, channel_id, query, answer, steps)
        return ChatResponse(
            run_id=run_id,
            answer=answer,
            video_id="not_applicable",
            risk_score=0.0,
            risk_level="not_applicable",
            top_factors=[],
            citations=[self._citation(chunk) for chunk in citations],
            agent_steps=steps,
        )

    def _persist_run(
        self,
        session: Session,
        run_id: str,
        channel_id: str,
        query: str,
        answer: str,
        steps: list[AgentStepResult],
    ) -> None:
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

    def _citation(self, chunk: RetrievedChunk) -> Citation:
        return Citation(
            title=chunk.title,
            chunk_id=chunk.chunk_id,
            score=chunk.score,
            text=chunk.text,
        )

    def _guidance_answer(self, query: str, citations: list[RetrievedChunk]) -> str:
        if not citations:
            return "I could not find relevant creator guidance yet. Ingest the documents and try again."

        titles = ", ".join(dict.fromkeys(chunk.title for chunk in citations))
        query_lower = query.lower()
        if "ctr" in query_lower or "thumbnail" in query_lower or "title" in query_lower:
            recommendation = (
                "Focus first on the title-thumbnail promise: make one clear reason to click, "
                "remove visual clutter, and ensure the opening proves that promise quickly."
            )
        elif "retention" in query_lower or "watch" in query_lower:
            recommendation = (
                "Improve the first 30 seconds: start with the payoff, remove slow setup, "
                "and compare pacing against recent videos with stronger retention."
            )
        elif "upload" in query_lower or "consistency" in query_lower:
            recommendation = (
                "Stabilize the publishing rhythm before experimenting heavily, then review each "
                "upload after early impressions and retention have settled."
            )
        else:
            recommendation = (
                "Use the retrieved guidance as the next decision filter: check topic fit, packaging clarity, "
                "and whether the video satisfies the viewer promise."
            )

        return f"Relevant guidance came from {titles}. {recommendation}"

    def _classify_intent(self, query: str) -> QueryIntent:
        normalized = query.lower().strip()
        product_terms = [
            "how does this product work",
            "how does this work",
            "what is this",
            "what does this app do",
            "explain this product",
            "how to use",
            "help",
            "hello",
            "hi",
        ]
        guidance_terms = [
            "monetization",
            "policy",
            "thumbnail",
            "title",
            "retention",
            "ctr",
            "upload",
            "consistency",
            "best practice",
            "strategy",
            "how should i improve",
        ]
        analysis_terms = [
            "underperform",
            "latest video",
            "last video",
            "risk",
            "views",
            "watch time",
            "channel growth",
            "my videos",
            "my channel",
        ]

        if any(term in normalized for term in product_terms):
            return QueryIntent.PRODUCT_HELP
        if any(term in normalized for term in analysis_terms):
            return QueryIntent.VIDEO_ANALYSIS
        if any(term in normalized for term in guidance_terms):
            return QueryIntent.CREATOR_GUIDANCE
        return QueryIntent.CREATOR_GUIDANCE

    def _step(
        self,
        order: int,
        tool_name: str,
        input_payload: dict[str, object],
        summary: str,
    ) -> AgentStepResult:
        return AgentStepResult(step=order, tool=tool_name, summary=summary, input_payload=input_payload)
