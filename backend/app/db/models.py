from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Channel(Base):
    __tablename__ = "channels"

    channel_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    channel_name: Mapped[str] = mapped_column(String(255), nullable=False)
    niche: Mapped[str] = mapped_column(String(120), nullable=False)
    subscriber_count: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    videos: Mapped[list["Video"]] = relationship(back_populates="channel")
    channel_metrics: Mapped[list["ChannelMetricDaily"]] = relationship(back_populates="channel")


class Video(Base):
    __tablename__ = "videos"

    video_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    channel_id: Mapped[str] = mapped_column(ForeignKey("channels.channel_id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(120), nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False)

    channel: Mapped[Channel] = relationship(back_populates="videos")
    daily_metrics: Mapped[list["VideoMetricDaily"]] = relationship(back_populates="video")
    predictions: Mapped[list["Prediction"]] = relationship(back_populates="video")


class VideoMetricDaily(Base):
    __tablename__ = "video_metrics_daily"

    metric_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    video_id: Mapped[str] = mapped_column(ForeignKey("videos.video_id"), nullable=False)
    metric_date: Mapped[date] = mapped_column(Date, nullable=False)
    views: Mapped[int] = mapped_column(Integer, nullable=False)
    impressions: Mapped[int] = mapped_column(Integer, nullable=False)
    ctr: Mapped[float] = mapped_column(Float, nullable=False)
    avg_view_duration: Mapped[float] = mapped_column(Float, nullable=False)
    retention_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    likes: Mapped[int] = mapped_column(Integer, nullable=False)
    comments: Mapped[int] = mapped_column(Integer, nullable=False)
    subscribers_gained: Mapped[int] = mapped_column(Integer, nullable=False)
    subscribers_lost: Mapped[int] = mapped_column(Integer, nullable=False)

    video: Mapped[Video] = relationship(back_populates="daily_metrics")


class ChannelMetricDaily(Base):
    __tablename__ = "channel_metrics_daily"

    metric_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    channel_id: Mapped[str] = mapped_column(ForeignKey("channels.channel_id"), nullable=False)
    metric_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_views: Mapped[int] = mapped_column(Integer, nullable=False)
    total_watch_time: Mapped[int] = mapped_column(Integer, nullable=False)
    subscriber_count: Mapped[int] = mapped_column(Integer, nullable=False)
    avg_ctr: Mapped[float] = mapped_column(Float, nullable=False)
    avg_retention: Mapped[float] = mapped_column(Float, nullable=False)

    channel: Mapped[Channel] = relationship(back_populates="channel_metrics")


class Prediction(Base):
    __tablename__ = "predictions"

    prediction_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    video_id: Mapped[str] = mapped_column(ForeignKey("videos.video_id"), nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(32), nullable=False)
    top_factors: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    video: Mapped[Video] = relationship(back_populates="predictions")


class AgentRun(Base):
    __tablename__ = "agent_runs"

    run_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    channel_id: Mapped[str] = mapped_column(ForeignKey("channels.channel_id"), nullable=False)
    user_query: Mapped[str] = mapped_column(Text, nullable=False)
    final_answer: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class AgentStep(Base):
    __tablename__ = "agent_steps"

    step_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("agent_runs.run_id"), nullable=False)
    step_order: Mapped[int] = mapped_column(Integer, nullable=False)
    tool_name: Mapped[str] = mapped_column(String(120), nullable=False)
    input_payload: Mapped[str] = mapped_column(Text, nullable=False)
    output_summary: Mapped[str] = mapped_column(Text, nullable=False)


class Document(Base):
    __tablename__ = "documents"

    document_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    source_type: Mapped[str] = mapped_column(String(80), nullable=False)
    ingested_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    chunk_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.document_id"), nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    qdrant_point_id: Mapped[str] = mapped_column(String(120), nullable=False)

