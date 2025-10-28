from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.services.kafka.kafka_service import kafka_service
from src.services.kafka.config import kafka_settings
from src.database import init_es_async_client



@asynccontextmanager
async def lifespan(app: FastAPI):
  
  es_client = await init_es_async_client()
  
  print("Database connected succesfully")
  
  await kafka_service.start_producer()
  await kafka_service.start_consumer([kafka_settings.topic_in])
  
  print("Kafka connect succesfully")
  
  yield
  
  await kafka_service.close()
  await es_client.close()