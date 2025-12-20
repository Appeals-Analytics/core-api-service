from sqlalchemy import String, DateTime, Float, Index, text as sql_text
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from src.database import Base
import uuid
from src.schemas import (
  SentimentEnum,
  EmotionEnum,
  CategoryLevel1Enum,
  CategoryLevel2Enum,
)


sentiment_enum = Enum(SentimentEnum, name="sentiment_enum")
emotion_enum = Enum(EmotionEnum, name="emotion_enum")
category_level_1_enum = Enum(CategoryLevel1Enum, name="category_level_1_enum")
category_level_2_enum = Enum(CategoryLevel2Enum, name="category_level_2_enum")


class Message(Base):
  __tablename__ = "messages"

  id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
  external_id: Mapped[str] = mapped_column(String, index=True)

  created_at: Mapped[datetime] = mapped_column(DateTime)
  event_date: Mapped[datetime] = mapped_column(DateTime, index=True)

  source: Mapped[str] = mapped_column(String)
  user_id: Mapped[str] = mapped_column(String, index=True)

  text: Mapped[str] = mapped_column(String)
  cleaned_text: Mapped[str] = mapped_column(String)

  lang_code: Mapped[str] = mapped_column(String, index=True)
  lang_score: Mapped[float] = mapped_column(Float)

  sentiment_label: Mapped[SentimentEnum] = mapped_column(sentiment_enum, index=True)
  sentiment_score: Mapped[float] = mapped_column(Float)

  emotion_label: Mapped[EmotionEnum] = mapped_column(emotion_enum, index=True)
  emotion_score: Mapped[float] = mapped_column(Float)

  category_level_1: Mapped[CategoryLevel1Enum] = mapped_column(category_level_1_enum, index=True)

  category_level_2: Mapped[list[CategoryLevel2Enum]] = mapped_column(ARRAY(category_level_2_enum))

  content_hash: Mapped[str] = mapped_column(String(64), index=True, nullable=True)

  __table_args__ = (
    Index("ix_messages_cat_level_2", category_level_2, postgresql_using="gin"),
    Index(
      "ix_messages_content_search",
      sql_text("to_tsvector('simple', cleaned_text)"),
      postgresql_using="gin",
    ),
  )
