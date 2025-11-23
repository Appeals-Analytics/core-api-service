from sqlalchemy import Column, Integer, String, DateTime, Float, Index, text as sql_text
from sqlalchemy.dialects.postgresql import ARRAY, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from src.database import Base
import uuid

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

    # ML Результаты (Язык, Сентимент, Эмоция)
    lang_code: Mapped[str] = mapped_column(String)
    lang_score: Mapped[float] = mapped_column(Float)

    sentiment_label: Mapped[str] = mapped_column(String)
    sentiment_score: Mapped[float] = mapped_column(Float)

    emotion_label: Mapped[str] = mapped_column(String)
    emotion_score: Mapped[float] = mapped_column(Float)

    category_level_1: Mapped[str] = mapped_column(String, index=True)
    
    category_level_2: Mapped[list[str]] = mapped_column(ARRAY(String))

    __table_args__ = (
        Index('ix_messages_cat_level_2', category_level_2, postgresql_using='gin'),
        
        Index(
            'ix_messages_content_search',
            sql_text("to_tsvector('simple', cleaned_text)"), 
            postgresql_using='gin'
        ),
    )