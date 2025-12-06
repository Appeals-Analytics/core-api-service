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
from pydantic import BaseModel, ConfigDict, computed_field
from typing import List


class EmotionCountedItem(BaseModel):
  emotion_label: EmotionEnum
  count: int
  total_count: int

  model_config = ConfigDict(from_attributes=True)

  @computed_field
  @property
  def emotion_label_ru(self) -> str:
    return EMOTION_TRANSLATIONS.get(self.emotion_label, self.emotion_label.value)


class SentimentCountedItem(BaseModel):
  sentiment_label: SentimentEnum
  count: int
  total_count: int

  model_config = ConfigDict(from_attributes=True)

  @computed_field
  @property
  def sentiment_label_ru(self) -> str:
    return SENTIMENT_TRANSLATIONS.get(self.sentiment_label, self.sentiment_label.value)


class CategoryCountedItem(BaseModel):
  label: CategoryLevel1Enum | CategoryLevel2Enum
  count: int
  total_count: int
  emotions: dict[EmotionEnum, int]

  @computed_field
  @property
  def label_ru(self) -> str:
    return CATEGORY_LEVEL_1_TRANSLATIONS.get(self.label, None) or CATEGORY_LEVEL_2_TRANSLATIONS.get(
      self.label, None
    )

  @computed_field
  @property
  def emotions_ru(self) -> dict[str, int]:
    return {EMOTION_TRANSLATIONS.get(emotion): count for emotion, count in self.emotions.items()}

  model_config = ConfigDict(from_attributes=True)


CategoriesAggregatedData = List[CategoryCountedItem]

EmotionsAggregatedData = List[EmotionCountedItem]

SentimentsAggregatedData = List[SentimentCountedItem]
