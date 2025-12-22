from src.database.models.message import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func, between
import sqlalchemy
from src.schemas.order_enum import OrderEnum
from src.api.message.schemas import MessageQueryFilter
from src.api.dashboard.schemas import (
  EmotionsAggregationQeury,
  SentimentAggregationQuery,
  CategoriesLevel1AggregationQuery,
  CategoriesLevel2AggregationQuery,
  EmotionDynamicsQuery
)
from datetime import datetime


class MessageRepository:
  def __init__(self, db: AsyncSession):
    self.db = db

  async def create_message(self, message_data: dict) -> Message:
    """Create a new message in the database"""
    if "created_at" not in message_data or message_data["created_at"] is None:
      message_data["created_at"] = datetime.utcnow()
    message = Message(**message_data)
    self.db.add(message)
    await self.db.commit()
    return message

  async def get_message(self, message_id: str) -> Message | None:
    """Get a message by ID"""
    result = await self.db.execute(select(Message.__table__.columns).where(Message.id == message_id))
    return result.scalar_one_or_none()

  async def get_messages(self, params: MessageQueryFilter) -> list[Message]:
    """Get messages with pagination"""

    query = select(Message.__table__.columns).filter(
      between(Message.event_date, params.start_date, params.end_date)
    )

    if params.category_level_1 is not None:
      query = query.filter(Message.category_level_1 == params.category_level_1)
    if params.category_level_2 is not None:
      query = query.filter(Message.category_level_2.contains([params.category_level_2]))
    if params.emotion_label is not None:
      query = query.filter(Message.emotion_label.in_(params.emotion_label))
    if params.source is not None:
      query = query.filter(Message.source == params.source)
    if params.user_id is not None:
      query = query.filter(Message.user_id == params.user_id)
    if params.search is not None:
      search_query = func.plainto_tsquery("simple", params.search)
      query = query.filter(func.to_tsvector("simple", Message.cleaned_text).op("@@")(search_query))
    if params.sentiment_label is not None:
      query = query.filter(Message.sentiment_label.in_(params.sentiment_label))

    result = await self.db.execute(query)

    return result.mappings().all()

  async def get_aggregated_messages_by_emotion(self, params: EmotionsAggregationQeury):
    """Get count of messages grouped by emotion for a given period"""

    query = select(
      Message.emotion_label,
      func.count(Message.id).label("count"),
      func.sum(func.count(Message.id)).over().label("total_count"),
    ).filter(between(Message.event_date, params.start_time, params.end_time))

    if params.level1_category is not None:
      query = query.filter(Message.category_level_1 == params.level1_category)
    if params.level2_category is not None:
      query = query.filter(Message.category_level_2.contains([params.level2_category]))
    if params.emotion_label is not None:
      query = query.filter(Message.emotion_label.in_(params.emotion_label))
    if params.sentiment_label is not None:
      query = query.filter(Message.sentiment_label.in_(params.sentiment_label))

    query = query.group_by(Message.emotion_label)

    result = await self.db.execute(query)

    return result.mappings().all()

  async def get_aggregated_messages_by_sentiment(self, params: SentimentAggregationQuery):
    """Get count of messages grouped by sentiment for a given period"""
    query = select(
      Message.sentiment_label,
      func.count(Message.id).label("count"),
      func.sum(func.count(Message.id)).over().label("total_count"),
    ).filter(between(Message.event_date, params.start_time, params.end_time))

    if params.level1_category is not None:
      query = query.filter(Message.category_level_1 == params.level1_category)
    if params.level2_category is not None:
      query = query.filter(Message.category_level_2.contains([params.level2_category]))
    if params.emotion_label is not None:
      query = query.filter(Message.emotion_label.in_(params.emotion_label))
    if params.sentiment_label is not None:
      query = query.filter(Message.sentiment_label.in_(params.sentiment_label))

    query = query.group_by(Message.sentiment_label)

    result = await self.db.execute(query)
    return result.mappings().all()

  async def get_aggregated_messages_by_category_level1(self, params: CategoriesLevel1AggregationQuery):
    subq = (
      select(
        Message.category_level_1,
        func.lower(func.cast(Message.emotion_label, sqlalchemy.String)).label("emotion_label"),
        func.count(Message.id).label("emotion_count"),
      )
      .filter(between(Message.event_date, params.start_time, params.end_time))
      .group_by(Message.category_level_1, Message.emotion_label)
      .subquery()
    )

    query = select(
      subq.c.category_level_1.label("label"),
      func.sum(subq.c.emotion_count).label("count"),
      func.sum(func.sum(subq.c.emotion_count)).over().label("total_count"),
      func.json_object_agg(subq.c.emotion_label, subq.c.emotion_count).label("emotions"),
    ).group_by(subq.c.category_level_1)

    if params.order_by == OrderEnum.ASC:
      query = query.order_by(func.sum(subq.c.emotion_count).asc())
    else:
      query = query.order_by(func.sum(subq.c.emotion_count).desc())

    result = await self.db.execute(query)
    return result.mappings().all()
  
  async def get_aggregated_messages_by_category_level2(self, params: CategoriesLevel2AggregationQuery):
    
    subq = (
      select(
        func.unnest(Message.category_level_2).label("level2"),
        func.lower(func.cast(Message.emotion_label, sqlalchemy.String)).label("emotion_label"),
        func.count(Message.id).label("emotion_count"),
      )
      .filter(Message.category_level_1 == params.level1_category)
      .filter(between(Message.event_date, params.start_time, params.end_time))
      .group_by(func.unnest(Message.category_level_2), Message.emotion_label)
      .subquery()
    )

    query = select(
      subq.c.level2.label("label"),
      func.sum(subq.c.emotion_count).label("count"),
      func.sum(func.sum(subq.c.emotion_count)).over().label("total_count"),
      func.json_object_agg(subq.c.emotion_label, subq.c.emotion_count).label("emotions"),
    ).group_by(subq.c.level2)
    
    if params.order_by == OrderEnum.ASC:
      query = query.order_by(func.sum(subq.c.emotion_count).asc())
    else:
      query = query.order_by(func.sum(subq.c.emotion_count).desc())

    result = await self.db.execute(query)
    return result.mappings().all()


  async def delete_message(self, id: str) -> None:
    """Delete message by ID"""
    await self.db.execute(delete(Message).where(Message.id == id))
    await self.db.commit()

  async def get_existing_hashes(self, hashes: list[str]) -> set[str]:
    """Get existing content hashes from the database"""
    if not hashes:
      return set()
    
    query = select(Message.content_hash).where(Message.content_hash.in_(hashes))
    result = await self.db.execute(query)
    return set(result.scalars().all())

  async def get_emotion_dynamics(self, params: EmotionDynamicsQuery):
    """Get aggregated emotion data grouped by time intervals"""
    trunc_date = func.date_trunc(params.granularity.value, Message.event_date).label("period")

    query = select(
      trunc_date,
      Message.emotion_label,
      func.count(Message.id).label("count"),
      func.avg(Message.sentiment_score).label("avg_sentiment"),
      func.avg(Message.emotion_score).label("avg_confidence"),
    ).filter(between(Message.event_date, params.start_time, params.end_time))

    if params.level1_category is not None:
      query = query.filter(Message.category_level_1 == params.level1_category)
    if params.level2_category is not None:
      query = query.filter(Message.category_level_2.contains([params.level2_category]))
    if params.emotion_label is not None:
      query = query.filter(Message.emotion_label.in_(params.emotion_label))
    if params.sentiment_label is not None:
      query = query.filter(Message.sentiment_label.in_(params.sentiment_label))
    if params.source is not None:
      query = query.filter(Message.source == params.source)
    if params.user_id is not None:
      query = query.filter(Message.user_id == params.user_id)

    query = query.group_by(trunc_date, Message.emotion_label).order_by(trunc_date.asc())

    result = await self.db.execute(query)
    return result.mappings().all()

