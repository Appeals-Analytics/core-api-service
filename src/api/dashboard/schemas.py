from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional
from src.schemas.order_enum import OrderEnum
from src.schemas import CategoryLevel1Enum, CategoryLevel2Enum


class BaseTimeQuery(BaseModel):
    __seven_days_ago__ = datetime.now() - timedelta(days=7)

    start_time: Optional[datetime] = Field(__seven_days_ago__)
    end_time: Optional[datetime] = Field(datetime.now())


class EmotionsAggregationQeury(BaseTimeQuery):
    def __init_subclass__(cls, **kwargs):
        return super().__init_subclass__(**kwargs)

    level1_category: Optional[CategoryLevel1Enum] = Field(
        None, description="Optional category for get emtions"
    )
    level2_category: Optional[CategoryLevel2Enum] = Field(
        None, description="Optional level2 category for get emtions"
    )


class SentimentAggregationQuery(BaseTimeQuery):
    def __init_subclass__(cls, **kwargs):
        return super().__init_subclass__(**kwargs)

    level1_category: Optional[CategoryLevel1Enum] = Field(
        None, description="Optional category for get sentiments"
    )
    level2_category: Optional[CategoryLevel2Enum] = Field(
        None, description="Optional level2 category for get sentiments"
    )


class CategoriesAggregationQuery(BaseTimeQuery):
    def __init_subclass__(cls, **kwargs):
        return super().__init_subclass__(**kwargs)

    level1_category: Optional[CategoryLevel1Enum] = Field(
        None, description="Optional category"
    )
    order_by: Optional[OrderEnum] = Field(OrderEnum.DESC)
