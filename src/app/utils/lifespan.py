from contextlib import asynccontextmanager
from fastapi import FastAPI
from services.kafka.kafka_service import kafka_service
from services.kafka.config import kafka_settings



@asynccontextmanager
async def lifespan(app: FastAPI):
  
  print("Database connected succesfully")
  
  await kafka_service.start_producer()
  await kafka_service.start_consumer([kafka_settings.topic_in])
  
  print("Kafka connect succesfully")
  
  yield
  
  await kafka_service.close()