from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from .responses import MessageResponse
from .schemas import MessageCreate
from .service import MessageService
from src.database import get_db

messages_router = APIRouter(prefix="/messages", tags=["messages"])

@messages_router.get("/", response_model=List[MessageResponse])
async def get_messages(skip: int = 0, limit: int = 100, db = Depends(get_db)):
  service = MessageService(db)
  return await service.get_messages(skip, limit)

@messages_router.get("/{id}")
async def get_message_by_id(id: str, db = Depends(get_db)) -> MessageResponse:
  service = MessageService(db)
  message = await service.get_message_by_id(id)
  if not message:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
  return message

@messages_router.post("/")
async def create_message(message: MessageCreate, db = Depends(get_db)) -> MessageResponse:
  service = MessageService(db)
  return await service.create_message(message)

@messages_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(id: str, db = Depends(get_db)):
  service = MessageService(db)
  await service.delete_message(id)
