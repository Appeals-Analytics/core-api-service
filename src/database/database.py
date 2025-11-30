from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.app.config import configs


class Base(DeclarativeBase):
    pass


engine = create_async_engine(configs.get_db_url(), echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, autoflush=True, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
