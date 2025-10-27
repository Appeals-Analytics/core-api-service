from src.services.kafka.kafka_service import kafka_service
from typing import List
import json

async def send_batch_to_kafka(*, data: List[dict], topic: str):
  
  json_data = json.dumps(data).encode("utf-8")
  await kafka_service.send_message(topic=topic, message=json_data)