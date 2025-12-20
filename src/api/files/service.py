import asyncio
import os

from src.services import (
  kafka_service,
  process_file as process_file_sync,
  kafka_settings,
  validate_file_structure as validate_file_structure_sync,
)
from src.services.file_upload.service import FileProcessorFactory
from pathlib import Path
from src.app.exceptions import BAD_REQUEST_EXCEPTION
from src.database.database import AsyncSessionLocal
from src.database.repositories.message import MessageRepository


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
    processor = await asyncio.to_thread(FileProcessorFactory.create, Path(file_path))
    
    df = await asyncio.to_thread(processor.read_data)

    await asyncio.to_thread(processor.validate_structure, df)
    
    total_rows = df.height
    batch_size = 2000
    local_seen_hashes = set()
    
    async with AsyncSessionLocal() as session:
      repo = MessageRepository(session)
      
      for i in range(0, total_rows, batch_size):
        chunk_df = df.slice(i, batch_size)
        
        batch_data = await asyncio.to_thread(processor.process_batch, chunk_df)
        
        if not batch_data:
          continue

        unique_batch = []
        for record in batch_data:
          if record.content_hash and record.content_hash not in local_seen_hashes:
            local_seen_hashes.add(record.content_hash)
            unique_batch.append(record)
        
        if not unique_batch:
          continue

        hashes_to_check = [r.content_hash for r in unique_batch if r.content_hash]
        existing_hashes = await repo.get_existing_hashes(hashes_to_check)
        
        final_batch = [r for r in unique_batch if r.content_hash not in existing_hashes]
        
        if not final_batch:
          continue

        messages = [record.model_dump() for record in final_batch]
        await kafka_service.send_messages(kafka_settings.topic_out, messages)

    os.remove(file_path)
