from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class MessageCreate(BaseModel):
    """Schema for creating a new message"""
    external_id: str = Field(..., description="External identifier for the message")
    event_date: datetime = Field(..., description="Date when the event occurred")
    source: str = Field(..., description="Source of the message")
    user_id: str = Field(..., description="User identifier")
    text: str = Field(..., description="Original message text")
    cleaned_text: str = Field(..., description="Cleaned/processed message text")

    lang_code: str = Field(..., description="Detected language code")
    lang_score: float = Field(..., ge=0.0, le=1.0, description="Language detection confidence score")

    sentiment_label: str = Field(..., description="Sentiment classification label")
    sentiment_score: float = Field(..., ge=0.0, le=1.0, description="Sentiment classification confidence score")

    emotion_label: str = Field(..., description="Emotion classification label")
    emotion_score: float = Field(..., ge=0.0, le=1.0, description="Emotion classification confidence score")

    category_level_1: str = Field(..., description="Primary category classification")
    category_level_2: List[str] = Field(..., description="Secondary category classifications")