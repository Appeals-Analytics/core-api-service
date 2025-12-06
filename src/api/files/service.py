import asyncio
import os

from src.services import (
  kafka_service,
  process_file as process_file_sync,
  kafka_settings,
  validate_file_structure as validate_file_structure_sync,
)
from src.app.exceptions import BAD_REQUEST_EXCEPTION


class FilesService:
  @staticmethod
  async def validate_file(file_path: str):
    try:
      await asyncio.to_thread(validate_file_structure_sync, file_path)
    except ValueError as e:
      raise BAD_REQUEST_EXCEPTION(detail=str(e))

  @staticmethod
  async def process_file(file_path: str) -> dict:
    return await asyncio.to_thread(process_file_sync, file_path)

  @staticmethod
  async def process_and_send_to_kafka(file_path: str):
    result = await asyncio.to_thread(process_file_sync, file_path)
    os.remove(file_path)

    data = result["data"]
    messages = [record.model_dump_json() for record in data]
    for message in messages:
      await kafka_service.send_message(kafka_settings.topic_out, message)
