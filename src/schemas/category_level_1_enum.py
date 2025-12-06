from enum import Enum


class CategoryLevel1Enum(Enum):
  BEFORE_FLIGHT = "before_flight"
  DEPARTURE_ARRIVAL = "departure_arrival"
  ON_BOARD = "on_board"
  AFTER_FLIGHT = "after_flight"
  LOYALTY_SALES = "loyalty_sales"
  TECHNICAL_ISSUES = "technical_issues"
  FEEDBACK = "feedback"
  SERVICE = "service"
  OTHER = "other"


CATEGORY_LEVEL_1_TRANSLATIONS: dict[CategoryLevel1Enum, str] = {
  CategoryLevel1Enum.BEFORE_FLIGHT: "До Вылета",
  CategoryLevel1Enum.DEPARTURE_ARRIVAL: "Вылет Прилет",
  CategoryLevel1Enum.ON_BOARD: "На борту",
  CategoryLevel1Enum.AFTER_FLIGHT: "После вылета",
  CategoryLevel1Enum.LOYALTY_SALES: "Лояльность и продажи",
  CategoryLevel1Enum.TECHNICAL_ISSUES: "Технические вопросы",
  CategoryLevel1Enum.FEEDBACK: "Обратная связь",
  CategoryLevel1Enum.SERVICE: "Сервисные",
  CategoryLevel1Enum.OTHER: "Другое",
}
