from enum import Enum


class EmotionEnum(Enum):
  ANGER = "anger"
  FEAR = "fear"
  DISGUST = "disgust"
  JOY = "joy"
  SADNESS = "sadness"
  SURPRISE = "surprise"
  GUILT = "guilt"
  INTEREST = "interest"
  NEUTRAL = "neutral"


EMOTION_TRANSLATIONS: dict[EmotionEnum, str] = {
  EmotionEnum.ANGER: "Гнев",
  EmotionEnum.FEAR: "Страх",
  EmotionEnum.DISGUST: "Отвращение",
  EmotionEnum.JOY: "Радость",
  EmotionEnum.SADNESS: "Грусть",
  EmotionEnum.SURPRISE: "Удивление",
  EmotionEnum.GUILT: "Вина",
  EmotionEnum.INTEREST: "Интерес",
  EmotionEnum.NEUTRAL: "Нейтральный",
}
