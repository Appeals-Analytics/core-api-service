from sqlalchemy.ext.asyncio import AsyncConnection
from src.database.repositories.message import MessageRepository
from .schemas import (
  EmotionsAggregationQeury,
  SentimentAggregationQuery,
  CategoriesLevel1AggregationQuery,
  CategoriesLevel2AggregationQuery,
  LEVEL_1_TO_LEVEL_2,
)
from .responses import (
  SentimentsAggregatedData,
  EmotionsAggregatedData,
  CategoriesAggregatedData,
  EmotionCountedItem,
  SentimentCountedItem,
  CategoryCountedItem,
)
from src.schemas import (
  EmotionEnum,
  SentimentEnum,
  CategoryLevel1Enum,
  CategoryLevel2Enum,
)


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

    return result

  @classmethod
  async def get_aggregated_level_2_categories(
    cls, db: AsyncConnection, params: CategoriesLevel2AggregationQuery
  ) -> CategoriesAggregatedData:
    data = await MessageRepository(db).get_aggregated_messages_by_category_level2(params)

    data_map = {item.label: item for item in data}
    total_count = data[0].total_count if data else 0

    if params.level1_category:
      categories_to_show = LEVEL_1_TO_LEVEL_2.get(params.level1_category, [])
    else:
      categories_to_show = list(CategoryLevel2Enum)

    result = []
    for category in categories_to_show:
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

    return result
