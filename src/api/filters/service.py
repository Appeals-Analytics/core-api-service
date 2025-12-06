from src.schemas import (
  CategoryLevel2Enum,
  CategoryLevel1Enum,
  SentimentEnum,
  EmotionEnum,
  EMOTION_TRANSLATIONS,
  CATEGORY_LEVEL_1_TRANSLATIONS,
  CATEGORY_LEVEL_2_TRANSLATIONS,
  SENTIMENT_TRANSLATIONS,
)


class FiltersService:
  @classmethod
  def get_emotions_filters(cls) -> dict[str, str]:
    return {emotion.value: EMOTION_TRANSLATIONS[emotion] for emotion in EmotionEnum}

  @classmethod
  def get_sentiments_filters(cls) -> dict[str, str]:
    return {sentiment.value: SENTIMENT_TRANSLATIONS[sentiment] for sentiment in SentimentEnum}

  @classmethod
  def get_categories_level1_filters(cls) -> dict[str, str]:
    return {
      category.value: CATEGORY_LEVEL_1_TRANSLATIONS[category] for category in CategoryLevel1Enum
    }

  @classmethod
  def get_categories_level2_filters(cls) -> dict[str, str]:
    return {
      category.value: CATEGORY_LEVEL_2_TRANSLATIONS[category] for category in CategoryLevel2Enum
    }
