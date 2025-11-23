from sqlalchemy.ext.asyncio import AsyncConnection
from .responses import MessageResponse
from database import MessageRepository
from .schemas import MessageCreate
class MessageService:
  
  def __init__(self, db: AsyncConnection):
    self.repository: MessageRepository = MessageRepository(db)
    
  async def get_message_by_id(self, id: str) -> MessageResponse:
    
    message = await self.repository.get_message(id)
    return self.repository.to_pydantic(message)
  
  async def create_message(self,  message: MessageCreate) -> MessageResponse:

    created_message = await self.repository.create_message(message)
    return self.repository.to_pydantic(created_message)

  async def get_messages(self, skip: int = 0, limit: int = 100) -> list[MessageResponse]:
    
    messages = await self.repository.get_messages(skip, limit)
    return [self.repository.to_pydantic(msg) for msg in messages]

  async def delete_message(self, id: str) -> None:
    
    await self.repository.delete_message(id)