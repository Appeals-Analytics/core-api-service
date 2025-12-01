import asyncio

from src.services import kafka_service, process_file as process_file_sync, kafka_settings


class FilesService:
    @staticmethod
    async def process_file(file_path: str) -> dict:
        return await asyncio.to_thread(process_file_sync, file_path)
    
    @staticmethod
    async def process_and_send_to_kafka(file_path: str):
        result = await asyncio.to_thread(process_file_sync, file_path)

        data = result['data']
        messages = [record.model_dump_json() for record in data]
        for message in messages:
            await kafka_service.send_message(kafka_settings.topic_out, message)