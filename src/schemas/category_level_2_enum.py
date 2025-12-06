from enum import Enum


class CategoryLevel2Enum(Enum):
  # Before Flight
  BOOKING = "booking"
  PAYMENT = "payment"
  REGISTRATION = "registration"
  BAGGAGE_BEFORE_FLIGHT = "baggage_before_flight"
  DOCUMENTS = "documents"

  # Departure / Arrival
  FLIGHT_STATUS = "flight_status"
  FLIGHT_DELAY = "flight_delay"
  FLIGHT_CANCELLATION = "flight_cancellation"
  HOTEL_TRANSFER = "hotel_transfer"
  BAGGAGE_SEARCH = "baggage_search"

  # On Board
  CABIN_SERVICE = "cabin_service"
  CABIN_CLEANLINESS = "cabin_cleanliness"
  CABIN_COMFORT = "cabin_comfort"
  CABIN_FOOD = "cabin_food"
  CABIN_ENTERTAINMENT = "cabin_entertainment"
  CABIN_BAGGAGE = "cabin_baggage"

  # After Flight
  TICKET_REFUND = "ticket_refund"
  TICKET_EXCHANGE = "ticket_exchange"
  COMPENSATION = "compensation"
  LOST_PROPERTY = "lost_property"

  # Loyalty & Sales
  LOYALTY_PROGRAM = "loyalty_program"
  PROMOTIONS_FARES = "promotions_fares"

  # Technical Issues
  WEBSITE_APP_ISSUES = "website_app_issues"
  BOT_ISSUES = "bot_issues"

  # Feedback
  COMPLAINT = "complaint"
  THANK_YOU = "thank_you"
  SUGGESTION = "suggestion"
  ESCALATION = "escalation"

  # Service
  GREETING = "greeting"
  FAREWELL = "farewell"

  # Other
  OTHER = "other"


CATEGORY_LEVEL_2_TRANSLATIONS: dict[CategoryLevel2Enum, str] = {
  # До Вылета
  CategoryLevel2Enum.BOOKING: "Бронирование",
  CategoryLevel2Enum.PAYMENT: "Оплата",
  CategoryLevel2Enum.REGISTRATION: "Регистрация",
  CategoryLevel2Enum.BAGGAGE_BEFORE_FLIGHT: "Багаж (до вылета)",
  CategoryLevel2Enum.DOCUMENTS: "Документы",
  # Вылет Прилет
  CategoryLevel2Enum.FLIGHT_STATUS: "Статус рейса",
  CategoryLevel2Enum.FLIGHT_DELAY: "Задержка рейса",
  CategoryLevel2Enum.FLIGHT_CANCELLATION: "Отмена рейса",
  CategoryLevel2Enum.HOTEL_TRANSFER: "Гостиница трансфер",
  CategoryLevel2Enum.BAGGAGE_SEARCH: "Поиск багажа",
  # На борту
  CategoryLevel2Enum.CABIN_SERVICE: "Обслуживание борт",
  CategoryLevel2Enum.CABIN_CLEANLINESS: "Чистота борт",
  CategoryLevel2Enum.CABIN_COMFORT: "Комфорт борт",
  CategoryLevel2Enum.CABIN_FOOD: "Питание борт",
  CategoryLevel2Enum.CABIN_ENTERTAINMENT: "Развлечения борт",
  CategoryLevel2Enum.CABIN_BAGGAGE: "Багаж борт",
  # После вылета
  CategoryLevel2Enum.TICKET_REFUND: "Возврат билета",
  CategoryLevel2Enum.TICKET_EXCHANGE: "Обмен билета",
  CategoryLevel2Enum.COMPENSATION: "Компенсация",
  CategoryLevel2Enum.LOST_PROPERTY: "Потерянная собственность",
  # Лояльность и продажи
  CategoryLevel2Enum.LOYALTY_PROGRAM: "Программа лояльности",
  CategoryLevel2Enum.PROMOTIONS_FARES: "Акции тарифы",
  # Технические вопросы
  CategoryLevel2Enum.WEBSITE_APP_ISSUES: "Работа сайта приложения",
  CategoryLevel2Enum.BOT_ISSUES: "Работа бота",
  # Обратная связь
  CategoryLevel2Enum.COMPLAINT: "Жалоба",
  CategoryLevel2Enum.THANK_YOU: "Благодарность",
  CategoryLevel2Enum.SUGGESTION: "Предложение",
  CategoryLevel2Enum.ESCALATION: "Эскалация",
  # Сервисные
  CategoryLevel2Enum.GREETING: "Приветствие",
  CategoryLevel2Enum.FAREWELL: "Прощание",
  # Другое
  CategoryLevel2Enum.OTHER: "Другое",
}
