from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.ml.predict import predict_video_risk

router = APIRouter(prefix="/predictions", tags=["predictions"])


class VideoRiskRequest(BaseModel):
    video_id: str = Field(examples=["video_104"])


class VideoRiskResponse(BaseModel):
    video_id: str
    risk_score: float
    risk_level: str
    top_factors: list[str]


@router.post("/video-risk", response_model=VideoRiskResponse)
def create_video_risk_prediction(
    request: VideoRiskRequest,
    db: Session = Depends(get_db),
) -> VideoRiskResponse:
    try:
        prediction = predict_video_risk(db, request.video_id)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail="Video risk model is not trained. Run `python -m app.ml.train` first.",
        ) from exc
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return VideoRiskResponse(
        video_id=prediction.video_id,
        risk_score=prediction.risk_score,
        risk_level=prediction.risk_level,
        top_factors=prediction.top_factors,
    )
