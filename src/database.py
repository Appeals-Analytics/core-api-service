from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.config import configs

DATABASE_URL = configs.get_db_url()

engine = create_async_engine(url=DATABASE_URL)

async_session = sessionmaker(engine, class_=AsyncConnection, expire_on_commit=False)

class Base(DeclarativeBase):
  pass