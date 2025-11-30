from fastapi import APIRouter, Depends, status, HTTPException, Query
from typing import List, Annotated
from .responses import MessageResponse
from .schemas import MessageCreate, MessageQueryFilter
from .service import MessageService
from src.database import get_db

messages_router = APIRouter(prefix="/messages", tags=["messages"])


@messages_router.get("/", response_model=List[MessageResponse])
async def get_messages(
    params: Annotated[MessageQueryFilter, Query()], db=Depends(get_db)
):
    return await MessageService.get_messages(db, params)


@messages_router.get("/{id}", response_model=MessageResponse)
async def get_message_by_id(id: str, db=Depends(get_db)):
    message = await MessageService.get_message_by_id(db, id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        )
    return message


@messages_router.post("/", response_model=MessageResponse)
async def create_message(message: MessageCreate, db=Depends(get_db)):
    return await MessageService.create_message(db, message)


@messages_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(id: str, db=Depends(get_db)):
    await MessageService.delete_message(db, id)
