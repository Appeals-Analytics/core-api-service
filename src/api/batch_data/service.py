from src.services.kafka.kafka_service import kafka_service
from typing import List


async def send_batch_to_kafka(*, data: List[str], topic: str):
    for item in data:
        await kafka_service.send_message(topic=topic, message=item)
