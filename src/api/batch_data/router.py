from fastapi import APIRouter, BackgroundTasks, status
from src.api.batch_data.exceptions import BATCH_TOO_LARGE_TO_PROCESSING
from src.api.batch_data.schemas import AppealItem
from typing import List
from src.services.kafka.config import kafka_settings
from src.api.batch_data.service import send_batch_to_kafka

batch_router = APIRouter(prefix="/batch-data", tags=["Batch Data"])

BATCH_MAX_SIZE = 1000


@batch_router.post("", status_code=status.HTTP_202_ACCEPTED)
async def process_batch_data(data: List[AppealItem], background_tasks: BackgroundTasks):
  if len(data) > BATCH_MAX_SIZE:
    raise BATCH_TOO_LARGE_TO_PROCESSING

  json_data = [item.model_dump_json() for item in data]

  background_tasks.add_task(send_batch_to_kafka, topic=kafka_settings.topic_out, data=json_data)
  return {"status": "accepted", "count": len(data)}
