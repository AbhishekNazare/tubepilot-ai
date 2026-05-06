# Phase 06: React Dashboard

## Branch

```text
phase/06-react-dashboard
```

## Goal

Build the demo-ready frontend for asking questions, reviewing video risk, inspecting channel trends, and viewing agent steps.

## Scope

- Build app navigation.
- Add Ask AI page with chat responses, citations, risk score, and timeline preview.
- Add Video Risk Dashboard table.
- Add Channel Insights page with metric summaries.
- Add Agent Timeline page.
- Connect frontend API client to backend endpoints.
- Add loading, empty, and error states.

## Suggested Commits

```text
add dashboard navigation layout
build ask ai chat experience
add video risk dashboard
add channel insights view
add agent timeline page
connect frontend api client
```

## Files To Add Or Update

```text
frontend/src/App.tsx
frontend/src/pages/AskAI.tsx
frontend/src/pages/VideoRisk.tsx
frontend/src/pages/ChannelInsights.tsx
frontend/src/pages/AgentTimeline.tsx
frontend/src/components/ChatPanel.tsx
frontend/src/components/RiskTable.tsx
frontend/src/components/MetricCard.tsx
frontend/src/components/CitationCard.tsx
frontend/src/components/AgentStepTimeline.tsx
frontend/src/api/client.ts
```

## Acceptance Criteria

- User can ask the sample underperformance question.
- UI displays answer, citations, risk score, and tool timeline.
- Risk dashboard shows demo videos with top factors.
- Layout works on desktop and mobile.

## Verification

```bash
cd frontend && npm run build
cd frontend && npm run dev
```

## Push Plan

```bash
git switch main
git pull
git switch -c phase/06-react-dashboard
git push -u origin phase/06-react-dashboard
```

