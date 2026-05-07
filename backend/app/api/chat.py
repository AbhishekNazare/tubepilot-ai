from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.agents.creator_agent import CreatorAgent
from app.agents.schemas import ChatResponse
from app.db.session import get_db

router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    channel_id: str = Field(examples=["channel_001"])
    query: str = Field(examples=["Why did my latest video underperform?"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    try:
        return CreatorAgent().run(db, request.channel_id, request.query)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="Video risk model is not trained. Run `python -m app.ml.train` first.",
        ) from exc
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

