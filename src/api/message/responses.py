from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List


class MessageResponse(BaseModel):
    """Schema for message response"""
    id: str = Field(..., description="Unique message identifier")
    external_id: str = Field(..., description="External identifier for the message")
    created_at: datetime = Field(..., description="Timestamp when the message was created")
    event_date: datetime = Field(..., description="Date when the event occurred")
    source: str = Field(..., description="Source of the message")
    user_id: str = Field(..., description="User identifier")
    text: str = Field(..., description="Original message text")
    cleaned_text: str = Field(..., description="Cleaned/processed message text")

    lang_code: str = Field(..., description="Detected language code")
    lang_score: float = Field(..., description="Language detection confidence score")

    sentiment_label: str = Field(..., description="Sentiment classification label")
    sentiment_score: float = Field(..., description="Sentiment classification confidence score")

    emotion_label: str = Field(..., description="Emotion classification label")
    emotion_score: float = Field(..., description="Emotion classification confidence score")

    category_level_1: str = Field(..., description="Primary category classification")
    category_level_2: List[str] = Field(..., description="Secondary category classifications")

    model_config = ConfigDict(from_attributes=True)
