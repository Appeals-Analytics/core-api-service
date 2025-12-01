from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.services import kafka_service, kafka_settings
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Database connected succesfully")

    await kafka_service.start_producer()
    await kafka_service.start_consumer([kafka_settings.topic_in])

    asyncio.create_task(kafka_service.consume_and_save_messages())

    print("Kafka connect succesfully")

    yield

    await kafka_service.close()
