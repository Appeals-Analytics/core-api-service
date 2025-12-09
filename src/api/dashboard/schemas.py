from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional, List
from src.schemas.order_enum import OrderEnum
from src.schemas import CategoryLevel1Enum, CategoryLevel2Enum, EmotionEnum, SentimentEnum


class BaseTimeQuery(BaseModel):
  __seven_days_ago__ = datetime.now() - timedelta(days=7)

  start_time: Optional[datetime] = Field(__seven_days_ago__)
  end_time: Optional[datetime] = Field(datetime.now())


class BaseOrderQuery(BaseModel):
  order_by: Optional[OrderEnum] = Field(OrderEnum.DESC)


class EmotionsAggregationQeury(BaseTimeQuery):
  def __init_subclass__(cls, **kwargs):
    return super().__init_subclass__(**kwargs)

  level1_category: Optional[CategoryLevel1Enum] = Field(
    None, description="Optional category for get emtions"
  )
  level2_category: Optional[CategoryLevel2Enum] = Field(
    None, description="Optional level2 category for get emtions"
  )
  emotion_label: Optional[List[EmotionEnum]] = Field(None, description="Filter by emotion labels")
  sentiment_label: Optional[List[SentimentEnum]] = Field(None, description="Filter by sentiment labels")


class SentimentAggregationQuery(BaseTimeQuery):
  def __init_subclass__(cls, **kwargs):
    return super().__init_subclass__(**kwargs)

  level1_category: Optional[CategoryLevel1Enum] = Field(
    None, description="Optional category for get sentiments"
  )
  level2_category: Optional[CategoryLevel2Enum] = Field(
    None, description="Optional level2 category for get sentiments"
  )
  emotion_label: Optional[List[EmotionEnum]] = Field(None, description="Filter by emotion labels")
  sentiment_label: Optional[List[SentimentEnum]] = Field(None, description="Filter by sentiment labels")


class CategoriesLevel1AggregationQuery(BaseTimeQuery, BaseOrderQuery):
  def __init_subclass__(cls, **kwargs):
    return super().__init_subclass__(**kwargs)


class CategoriesLevel2AggregationQuery(BaseTimeQuery, BaseOrderQuery):
  def __init_subclass__(cls, **kwargs):
    return super().__init_subclass__(**kwargs)

  level1_category: CategoryLevel1Enum = Field(
    CategoryLevel1Enum.FEEDBACK, description="Optional category"
  )


LEVEL_1_TO_LEVEL_2 = {
  CategoryLevel1Enum.BEFORE_FLIGHT: [
    CategoryLevel2Enum.BOOKING,
    CategoryLevel2Enum.PAYMENT,
    CategoryLevel2Enum.REGISTRATION,
    CategoryLevel2Enum.BAGGAGE_BEFORE_FLIGHT,
    CategoryLevel2Enum.DOCUMENTS,
  ],
  CategoryLevel1Enum.DEPARTURE_ARRIVAL: [
    CategoryLevel2Enum.FLIGHT_STATUS,
    CategoryLevel2Enum.FLIGHT_DELAY,
    CategoryLevel2Enum.FLIGHT_CANCELLATION,
    CategoryLevel2Enum.HOTEL_TRANSFER,
    CategoryLevel2Enum.BAGGAGE_SEARCH,
  ],
  CategoryLevel1Enum.ON_BOARD: [
    CategoryLevel2Enum.CABIN_SERVICE,
    CategoryLevel2Enum.CABIN_CLEANLINESS,
    CategoryLevel2Enum.CABIN_COMFORT,
    CategoryLevel2Enum.CABIN_FOOD,
    CategoryLevel2Enum.CABIN_ENTERTAINMENT,
    CategoryLevel2Enum.CABIN_BAGGAGE,
  ],
  CategoryLevel1Enum.AFTER_FLIGHT: [
    CategoryLevel2Enum.TICKET_REFUND,
    CategoryLevel2Enum.TICKET_EXCHANGE,
    CategoryLevel2Enum.COMPENSATION,
    CategoryLevel2Enum.LOST_PROPERTY,
  ],
  CategoryLevel1Enum.LOYALTY_SALES: [
    CategoryLevel2Enum.LOYALTY_PROGRAM,
    CategoryLevel2Enum.PROMOTIONS_FARES,
  ],
  CategoryLevel1Enum.TECHNICAL_ISSUES: [
    CategoryLevel2Enum.WEBSITE_APP_ISSUES,
    CategoryLevel2Enum.BOT_ISSUES,
  ],
  CategoryLevel1Enum.FEEDBACK: [
    CategoryLevel2Enum.COMPLAINT,
    CategoryLevel2Enum.THANK_YOU,
    CategoryLevel2Enum.SUGGESTION,
    CategoryLevel2Enum.ESCALATION,
  ],
  CategoryLevel1Enum.SERVICE: [
    CategoryLevel2Enum.GREETING,
    CategoryLevel2Enum.FAREWELL,
  ],
  CategoryLevel1Enum.OTHER: [
    CategoryLevel2Enum.OTHER,
  ],
}
