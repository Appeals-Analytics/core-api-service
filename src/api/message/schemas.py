from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from src.schemas import (
    EmotionEnum,
    SentimentEnum,
    CategoryLevel1Enum,
    CategoryLevel2Enum,
)


def to_naive_utc(dt: datetime) -> datetime:
    """Convert datetime to naive UTC"""
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


class MessageCreate(BaseModel):
    """Schema for creating a new message"""

    external_id: str = Field(..., description="External identifier for the message")
    event_date: datetime = Field(..., description="Date when the event occurred")
    source: str = Field(..., description="Source of the message")
    user_id: str = Field(..., description="User identifier")
    text: str = Field(..., description="Original message text")
    cleaned_text: str = Field(..., description="Cleaned/processed message text")

    lang_code: str = Field(..., description="Detected language code")
    lang_score: float = Field(
        ..., ge=0.0, le=1.0, description="Language detection confidence score"
    )

    sentiment_label: SentimentEnum = Field(..., description="Sentiment classification label")
    sentiment_score: float = Field(
        ..., ge=0.0, le=1.0, description="Sentiment classification confidence score"
    )

    emotion_label: EmotionEnum = Field(..., description="Emotion classification label")
    emotion_score: float = Field(
        ..., ge=0.0, le=1.0, description="Emotion classification confidence score"
    )

    category_level_1: CategoryLevel1Enum = Field(
        ..., description="Primary category classification"
    )
    category_level_2: List[CategoryLevel2Enum] = Field(
        ..., description="Secondary category classifications"
    )

    @field_validator("event_date", mode="before")
    @classmethod
    def normalize_event_date(cls, v):
        if isinstance(v, str):
            v = datetime.fromisoformat(v.replace("Z", "+00:00"))
        return to_naive_utc(v)

    @field_validator("sentiment_label", mode="before")
    @classmethod
    def normalize_sentiment(cls, v):
        if isinstance(v, str):
            return SentimentEnum(v.lower())
        return v

    @field_validator("emotion_label", mode="before")
    @classmethod
    def normalize_emotion(cls, v):
        if isinstance(v, str):
            return EmotionEnum(v.lower())
        return v

    @field_validator("category_level_1", mode="before")
    @classmethod
    def normalize_category_level_1(cls, v):
        if isinstance(v, str):
            return CategoryLevel1Enum(v.lower())
        return v

    @field_validator("category_level_2", mode="before")
    @classmethod
    def normalize_category_level_2(cls, v):
        if isinstance(v, list):
            return [CategoryLevel2Enum(item.lower()) if isinstance(item, str) else item for item in v]
        return v


class MessageQueryFilter(BaseModel):
    _seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()

    start_date: Optional[datetime] = Field(
      _seven_days_ago, description="Start date for filtering messages"
    )
    end_date: Optional[datetime] = Field(
        datetime.now().isoformat(), description="End date for filtering messages"
    )
    sentiment_label: Optional[SentimentEnum] = Field(
        None, description="Sentiment label to filter by"
    )
    emotion_label: Optional[EmotionEnum] = Field(
        None, description="Emotion label to filter by"
    )
    category_level_1: Optional[CategoryLevel1Enum] = Field(
        None, description="Primary category to filter by"
    )
    category_level_2: Optional[List[CategoryLevel2Enum]] = Field(
        None, description="Secondary category to filter by"
    )
    user_id: Optional[str] = Field(None, description="User ID to filter by")
    source: Optional[str] = Field(None, description="Source to filter by")

    search: Optional[str] = Field(None, description="Search string")
