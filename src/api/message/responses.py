from pydantic import BaseModel, Field, ConfigDict, computed_field
from datetime import datetime
from typing import List

from src.schemas import (
  EmotionEnum,
  SentimentEnum,
  CategoryLevel1Enum,
  CategoryLevel2Enum,
  EMOTION_TRANSLATIONS,
  SENTIMENT_TRANSLATIONS,
  CATEGORY_LEVEL_1_TRANSLATIONS,
  CATEGORY_LEVEL_2_TRANSLATIONS,
)


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

  sentiment_label: SentimentEnum = Field(..., description="Sentiment classification label")
  sentiment_score: float = Field(..., description="Sentiment classification confidence score")

  emotion_label: EmotionEnum = Field(..., description="Emotion classification label")
  emotion_score: float = Field(..., description="Emotion classification confidence score")

  category_level_1: CategoryLevel1Enum = Field(..., description="Primary category classification")
  category_level_2: List[CategoryLevel2Enum] = Field(
    ..., description="Secondary category classifications"
  )

  model_config = ConfigDict(from_attributes=True)

  @computed_field
  @property
  def sentiment_label_ru(self) -> str:
    return SENTIMENT_TRANSLATIONS.get(self.sentiment_label, self.sentiment_label.value)

  @computed_field
  @property
  def emotion_label_ru(self) -> str:
    return EMOTION_TRANSLATIONS.get(self.emotion_label, self.emotion_label.value)

  @computed_field
  @property
  def category_level_1_ru(self) -> str:
    return CATEGORY_LEVEL_1_TRANSLATIONS.get(self.category_level_1, self.category_level_1.value)

  @computed_field
  @property
  def category_level_2_ru(self) -> List[str]:
    return [CATEGORY_LEVEL_2_TRANSLATIONS.get(cat, cat.value) for cat in self.category_level_2]
