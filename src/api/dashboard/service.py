from sqlalchemy.ext.asyncio import AsyncConnection
from src.database.repositories.message import MessageRepository
from .schemas import (
    EmotionsAggregationQeury,
    SentimentAggregationQuery,
    CategoriesAggregationQuery,
)
from .responses import (
    SentimentsAggregatedData,
    EmotionsAggregatedData,
    CategoriesAggregatedData,
)


class DashboardService:
    @classmethod
    async def get_aggregated_emotions(
        cls, db: AsyncConnection, params: EmotionsAggregationQeury
    ) -> EmotionsAggregatedData:
        return await MessageRepository(db).get_aggregated_messages_by_emotion(params)

    @classmethod
    async def get_aggregated_sentiments(
        cls, db: AsyncConnection, params: SentimentAggregationQuery
    ) -> SentimentsAggregatedData:
        return await MessageRepository(db).get_aggregated_messages_by_sentiment(params)

    @classmethod
    async def get_aggregated_level1_category_data(
        cls, db: AsyncConnection, params: CategoriesAggregationQuery
    ) -> CategoriesAggregatedData:
        return await MessageRepository(db).get_aggregated_messages_by_category(params)
