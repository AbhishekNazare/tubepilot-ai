import csv
from collections.abc import Callable
from datetime import date, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import Base, Channel, ChannelMetricDaily, Video, VideoMetricDaily

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _int(value: str) -> int:
    return int(value)


def _float(value: str) -> float:
    return float(value)


def _load_rows(
    session: Session,
    model: type[Any],
    rows: list[dict[str, str]],
    converters: dict[str, Callable[[str], Any]],
) -> int:
    objects = []
    for row in rows:
        values = {
            key: converters.get(key, lambda raw: raw)(value)
            for key, value in row.items()
        }
        objects.append(model(**values))

    session.add_all(objects)
    return len(objects)


def reset_database(engine: Engine) -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def seed_database(engine: Engine, data_dir: Path = DATA_DIR) -> dict[str, int]:
    reset_database(engine)

    with Session(engine) as session:
        counts = {
            "channels": _load_rows(
                session,
                Channel,
                _read_csv(data_dir / "channels.csv"),
                {"subscriber_count": _int, "created_at": _parse_datetime},
            ),
            "videos": _load_rows(
                session,
                Video,
                _read_csv(data_dir / "videos.csv"),
                {"published_at": _parse_datetime, "duration_seconds": _int},
            ),
            "video_metrics_daily": _load_rows(
                session,
                VideoMetricDaily,
                _read_csv(data_dir / "video_metrics_daily.csv"),
                {
                    "metric_date": _parse_date,
                    "views": _int,
                    "impressions": _int,
                    "ctr": _float,
                    "avg_view_duration": _float,
                    "retention_percentage": _float,
                    "likes": _int,
                    "comments": _int,
                    "subscribers_gained": _int,
                    "subscribers_lost": _int,
                },
            ),
            "channel_metrics_daily": _load_rows(
                session,
                ChannelMetricDaily,
                _read_csv(data_dir / "channel_metrics_daily.csv"),
                {
                    "metric_date": _parse_date,
                    "total_views": _int,
                    "total_watch_time": _int,
                    "subscriber_count": _int,
                    "avg_ctr": _float,
                    "avg_retention": _float,
                },
            ),
        }
        session.commit()
        return counts


def main() -> None:
    settings = get_settings()
    engine = create_engine(settings.database_url, pool_pre_ping=True)
    counts = seed_database(engine)
    print(counts)


if __name__ == "__main__":
    main()

