from sqlalchemy.ext.asyncio import AsyncConnection
from .responses import MessageResponse
from src.database.repositories.message import MessageRepository
from .schemas import MessageCreate, MessageQueryFilter


class MessageService:
    @classmethod
    async def get_message_by_id(cls, db: AsyncConnection, id: str) -> MessageResponse:
        message = await MessageRepository(db).get_message(id)
        return MessageResponse.model_validate(message)

    @classmethod
    async def create_message(
        cls, db: AsyncConnection, message: MessageCreate
    ) -> MessageResponse:
        message_dict = message.model_dump()
        created_message = await MessageRepository(db).create_message(message_dict)
        return MessageResponse.model_validate(created_message)

    @classmethod
    async def get_messages(
        self, db: AsyncConnection, params: MessageQueryFilter
    ) -> list[MessageResponse]:
        messages = await MessageRepository(db).get_messages(params)
        return [MessageResponse.model_validate(msg) for msg in messages]

    @classmethod
    async def delete_message(self, db: AsyncConnection, id: str) -> None:
        await MessageRepository(db).delete_message(id)
