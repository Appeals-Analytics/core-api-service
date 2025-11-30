from fastapi import APIRouter, Depends, Query
from typing import Annotated
from src.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from .service import DashboardService
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

dashboard_router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@dashboard_router.get(path="/emotions", response_model=EmotionsAggregatedData)
async def get_aggregated_emotions(
    params: Annotated[EmotionsAggregationQeury, Query()],
    db: AsyncSession = Depends(get_db),
):
    return await DashboardService.get_aggregated_emotions(db, params)


@dashboard_router.get(path="/sentiments", response_model=SentimentsAggregatedData)
async def get_aggregated_sentiments(
    params: Annotated[SentimentAggregationQuery, Query()],
    db: AsyncSession = Depends(get_db),
):
    return await DashboardService.get_aggregated_sentiments(db, params)


@dashboard_router.get(path="/categories", response_model=CategoriesAggregatedData)
async def get_level1_categories_aggregated(
    params: Annotated[CategoriesAggregationQuery, Query()],
    db: AsyncSession = Depends(get_db),
):
    return await DashboardService.get_aggregated_level1_category_data(db, params)
