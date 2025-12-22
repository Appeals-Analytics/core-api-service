from sqlalchemy.ext.asyncio import AsyncConnection
from src.database.repositories.message import MessageRepository
from .schemas import (
  EmotionsAggregationQeury,
  SentimentAggregationQuery,
  CategoriesLevel1AggregationQuery,
  CategoriesLevel2AggregationQuery,
  EmotionDynamicsQuery,
  LEVEL_1_TO_LEVEL_2,
)
from .responses import (
  SentimentsAggregatedData,
  EmotionsAggregatedData,
  CategoriesAggregatedData,
  EmotionCountedItem,
  SentimentCountedItem,
  CategoryCountedItem,
  EmotionDynamicsResponse,
  EmotionDynamicsPeriod,
  EmotionDynamicsItem,
  EmotionDynamicsMeta,
)
from src.schemas import (
  EmotionEnum,
  SentimentEnum,
  CategoryLevel1Enum,
  CategoryLevel2Enum,
  GranularityEnum,
  EMOTION_TRANSLATIONS,
)
from src.schemas.order_enum import OrderEnum
from datetime import timedelta


class DashboardService:
  @classmethod
  async def get_aggregated_emotions(
    cls, db: AsyncConnection, params: EmotionsAggregationQeury
  ) -> EmotionsAggregatedData:
    data = await MessageRepository(db).get_aggregated_messages_by_emotion(params)
    data_map = {item.emotion_label: item for item in data}
    total_count = data[0].total_count if data else 0

    return [
      EmotionCountedItem(
        emotion_label=emotion,
        count=data_map[emotion].count if emotion in data_map else 0,
        total_count=total_count,
      )
      for emotion in EmotionEnum
    ]

  @classmethod
  async def get_aggregated_sentiments(
    cls, db: AsyncConnection, params: SentimentAggregationQuery
  ) -> SentimentsAggregatedData:
    data = await MessageRepository(db).get_aggregated_messages_by_sentiment(params)
    data_map = {item.sentiment_label: item for item in data}
    total_count = data[0].total_count if data else 0

    return [
      SentimentCountedItem(
        sentiment_label=sentiment,
        count=data_map[sentiment].count if sentiment in data_map else 0,
        total_count=total_count,
      )
      for sentiment in SentimentEnum
    ]

  @classmethod
  async def get_aggregated_level_1_categories(
    cls, db: AsyncConnection, params: CategoriesLevel1AggregationQuery
  ) -> CategoriesAggregatedData:
    data = await MessageRepository(db).get_aggregated_messages_by_category_level1(params)

    data_map = {item.label: item for item in data}
    total_count = data[0].total_count if data else 0

    result = []
    for category in CategoryLevel1Enum:
      if category in data_map:
        item = data_map[category]
        emotions = {emotion: item.emotions.get(emotion.value, 0) for emotion in EmotionEnum}
        result.append(
          CategoryCountedItem(
            label=category, count=item.count, total_count=total_count, emotions=emotions
          )
        )
      else:
        result.append(
          CategoryCountedItem(
            label=category,
            count=0,
            total_count=total_count,
            emotions={emotion: 0 for emotion in EmotionEnum},
          )
        )

    result.sort(key=lambda x: x.count, reverse=params.order_by == OrderEnum.DESC)
    return result

  @classmethod
  async def get_aggregated_level_2_categories(
    cls, db: AsyncConnection, params: CategoriesLevel2AggregationQuery
  ) -> CategoriesAggregatedData:
    data = await MessageRepository(db).get_aggregated_messages_by_category_level2(params)
    print(len(data))
    data_map = {item.label: item for item in data}
    total_count = data[0].total_count if data else 0
    print(data_map)
    if params.level1_category:
      categories_to_show = LEVEL_1_TO_LEVEL_2.get(params.level1_category, [])
    else:
      categories_to_show = list(CategoryLevel2Enum)

    result = []
    for category in categories_to_show:
      if category.name in data_map:
        item = data_map[category.name]
        emotions = {emotion: item.emotions.get(emotion.value, 0) for emotion in EmotionEnum}
        result.append(
          CategoryCountedItem(
            label=category, count=item.count, total_count=total_count, emotions=emotions
          )
        )
      else:
        result.append(
          CategoryCountedItem(
            label=category,
            count=0,
            total_count=total_count,
            emotions={emotion: 0 for emotion in EmotionEnum},
          )
        )

    result.sort(key=lambda x: x.count, reverse=params.order_by == OrderEnum.DESC)
    print(len(result))
    return result

  @classmethod
  async def get_emotion_dynamics(
    cls, db: AsyncConnection, params: EmotionDynamicsQuery
  ) -> EmotionDynamicsResponse:
    raw_data = await MessageRepository(db).get_emotion_dynamics(params)

    grouped_data = {}
    for row in raw_data:
      period = row.period
      if period not in grouped_data:
        grouped_data[period] = {
          "total_count": 0,
          "weighted_sentiment": 0.0,
          "weighted_confidence": 0.0,
          "breakdown": {}
        }
      
      count = row.count
      grouped_data[period]["total_count"] += count
      grouped_data[period]["weighted_sentiment"] += row.avg_sentiment * count
      grouped_data[period]["weighted_confidence"] += row.avg_confidence * count
      
      grouped_data[period]["breakdown"][row.emotion_label] = {
        "count": count,
        "label_ru": EMOTION_TRANSLATIONS.get(row.emotion_label, row.emotion_label.value)
      }

    def align_date(dt, granularity):
      if granularity == GranularityEnum.HOUR:
        return dt.replace(minute=0, second=0, microsecond=0)
      elif granularity == GranularityEnum.DAY:
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
      elif granularity == GranularityEnum.WEEK:
        return (dt - timedelta(days=dt.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
      elif granularity == GranularityEnum.MONTH:
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
      return dt

    aligned_start = align_date(params.start_time, params.granularity)
    aligned_end = align_date(params.end_time, params.granularity)
    
    periods = []
    curr = aligned_start
    while curr <= aligned_end:
      periods.append(curr)
      if params.granularity == GranularityEnum.HOUR:
        curr += timedelta(hours=1)
      elif params.granularity == GranularityEnum.DAY:
        curr += timedelta(days=1)
      elif params.granularity == GranularityEnum.WEEK:
        curr += timedelta(weeks=1)
      elif params.granularity == GranularityEnum.MONTH:
        if curr.month == 12:
          curr = curr.replace(year=curr.year + 1, month=1)
        else:
          curr = curr.replace(month=curr.month + 1)

    response_data = []
    for period in periods:
      data = grouped_data.get(period)
      if data:
        total = data["total_count"]
        avg_sentiment = data["weighted_sentiment"] / total if total > 0 else 0
        avg_confidence = data["weighted_confidence"] / total if total > 0 else 0
        
        breakdown = {}
        for emotion, info in data["breakdown"].items():
          breakdown[emotion.value] = EmotionDynamicsItem(
            count=info["count"],
            percentage=(info["count"] / total) * 100 if total > 0 else 0,
            label_ru=info["label_ru"]
          )
        
        response_data.append(EmotionDynamicsPeriod(
          period_start=period,
          total_count=total,
          average_sentiment_score=avg_confidence,
          average_emotion_confidence=avg_sentiment,
          breakdown=breakdown
        ))
      else:
        response_data.append(EmotionDynamicsPeriod(
          period_start=period,
          total_count=0,
          average_sentiment_score=0,
          average_emotion_confidence=0,
          breakdown={}
        ))
            
    return EmotionDynamicsResponse(
      meta=EmotionDynamicsMeta(
        granularity=params.granularity.value,
        total_periods=len(response_data)
      ),
      data=response_data
    )

