from enum import Enum


class SentimentEnum(Enum):
  VERY_POSITIVE = "very_positive"
  VERY_NEGATIVE = "very_negative"
  POSITIVE = "positive"
  NEGATIVE = "negative"
  NEUTRAL = "neutral"


SENTIMENT_TRANSLATIONS: dict[SentimentEnum, str] = {
  SentimentEnum.POSITIVE: "Положительный",
  SentimentEnum.NEGATIVE: "Отрицательный",
  SentimentEnum.NEUTRAL: "Нейтральный",
  SentimentEnum.VERY_POSITIVE: "Очень положительный",
  SentimentEnum.VERY_NEGATIVE: "Очень отрицательный",
}
