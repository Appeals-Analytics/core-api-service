from enum import Enum


class SentimentEnum(Enum):
  POSITIVE = "positive"
  NEGATIVE = "negative"
  NEUTRAL = "neutral"


SENTIMENT_TRANSLATIONS: dict[SentimentEnum, str] = {
  SentimentEnum.POSITIVE: "Положительный",
  SentimentEnum.NEGATIVE: "Отрицательный",
  SentimentEnum.NEUTRAL: "Нейтральный",
}
