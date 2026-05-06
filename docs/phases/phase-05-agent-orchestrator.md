# Phase 05: Agent Orchestrator

## Branch

```text
phase/05-agent-orchestrator
```

## Goal

Combine analytics, prediction, RAG, and LLM response generation into one transparent workflow.

## Scope

- Define agent tool schemas.
- Implement tools for channel metrics, recent videos, video metrics, risk prediction, document search, and action planning.
- Add a deterministic first workflow before adding complex planning.
- Persist agent runs and tool steps.
- Add `POST /chat`.
- Return final answer, citations, risk score, and timeline.

## Suggested Commits

```text
define creator agent tool schemas
implement analytics and rag agent tools
add chat orchestration workflow
persist agent run timeline
test underperformance chat workflow
```

## Files To Add Or Update

```text
backend/app/agents/schemas.py
backend/app/agents/tools.py
backend/app/agents/creator_agent.py
backend/app/api/chat.py
backend/app/db/models.py
backend/tests/test_agent_tools.py
backend/tests/test_chat_workflow.py
```

## Acceptance Criteria

- Chat endpoint answers the README demo question.
- Response includes agent steps in execution order.
- Tool outputs are logged and persisted.
- Tests cover the latest-video underperformance workflow.

## Verification

```bash
cd backend && pytest tests/test_agent_tools.py tests/test_chat_workflow.py
```

## Push Plan

```bash
git switch main
git pull
git switch -c phase/05-agent-orchestrator
git push -u origin phase/05-agent-orchestrator
```

