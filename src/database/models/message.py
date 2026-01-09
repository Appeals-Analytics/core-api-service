from sqlalchemy.orm import Mapped, mapped_column
from clickhouse_sqlalchemy import engines, types
from datetime import datetime, timezone
from src.database import Base
import uuid
from src.schemas import (
  SentimentEnum,
  EmotionEnum,
  CategoryLevel1Enum,
  CategoryLevel2Enum,
)


class Message(Base):
  __tablename__ = "messages"
  __table_args__ = (engines.MergeTree(order_by=["event_date", "id"]),)

  id: Mapped[str] = mapped_column(types.String, primary_key=True, default=lambda: str(uuid.uuid4()))
  external_id: Mapped[str] = mapped_column(types.String)

  created_at: Mapped[datetime] = mapped_column(types.DateTime, default=datetime.now(timezone.utc))
  event_date: Mapped[datetime] = mapped_column(types.DateTime)

  source: Mapped[str] = mapped_column(types.String)
  user_id: Mapped[str] = mapped_column(types.String)

  text: Mapped[str] = mapped_column(types.String)
  cleaned_text: Mapped[str] = mapped_column(types.String)

  lang_code: Mapped[str] = mapped_column(types.String)
  lang_score: Mapped[float] = mapped_column(types.Float64)

  sentiment_label: Mapped[SentimentEnum] = mapped_column(types.String)
  sentiment_score: Mapped[float] = mapped_column(types.Float64)

  emotion_label: Mapped[EmotionEnum] = mapped_column(types.String)
  emotion_score: Mapped[float] = mapped_column(types.Float64)

  category_level_1: Mapped[CategoryLevel1Enum] = mapped_column(types.String)

  category_level_2: Mapped[list[CategoryLevel2Enum]] = mapped_column(types.Array(types.String))

  content_hash: Mapped[str] = mapped_column(types.String, nullable=True)
