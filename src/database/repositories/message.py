from src.database import Message
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.message.schemas import MessageCreate
from src.api.message.responses import MessageResponse
from sqlalchemy import select, delete


class MessageRepository:

  def __init__(self, db: AsyncSession):
    self.db = db

  async def create_message(self, message_data: MessageCreate) -> Message:
    """Create a new message in the database"""
    message_dict = message_data.model_dump()
    message = Message(**message_dict)
    await self.db.add(message)
    await self.db.commit()
    return message

  async def get_message(self, message_id: str) -> Message | None:
    """Get a message by ID"""
    return await self.db.execute(select(Message).where(Message.id == message_id))

  async def get_messages(self, skip: int = 0, limit: int = 100) -> list[Message]:
    """Get messages with pagination"""
    result = await self.db.execute(
        select(Message).offset(skip).limit(limit)
    )
    return result.scalars().all()
  
  async def delete_message(self, id: str) -> None:
    """Delete message by ID"""
    return await self.db.execute(delete(Message).where(Message.id == id))

  def to_pydantic(self, message: Message) -> MessageResponse:
    """Convert SQLAlchemy Message model to Pydantic MessageResponse"""
    return MessageResponse.model_validate(message)

  def from_pydantic(self, message: MessageCreate) -> dict:
    """Convert Pydantic MessageCreate to dict for SQLAlchemy"""
    return message.model_dump()