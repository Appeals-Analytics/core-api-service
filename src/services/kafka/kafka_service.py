import json
from typing import AsyncGenerator, Optional, Self
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from src.services.kafka.config import kafka_settings

class KafkaService:
  def __init__(self: Self):
    self.producer: Optional[AIOKafkaProducer]
    self.consumer: Optional[AIOKafkaConsumer]

  async def start_producer(self: Self):

    producer_config = {
      "bootstrap_servers": kafka_settings.bootstrap_servers,
      "security_protocol": kafka_settings.security_protocol,
      "sasl_mechanism": kafka_settings.sasl_mechanism,
      "sasl_plain_username": kafka_settings.sasl_plain_username,
      "sasl_plain_password": kafka_settings.sasl_plain_password,
      "value_serializer": lambda v: json.dumps(v).encode('utf-8'),
    }

    self.producer = AIOKafkaProducer(**producer_config)
    await self.producer.start()

  async def start_consumer(self: Self, topics: list[str]):

      consumer_config = {
          "bootstrap_servers": kafka_settings.bootstrap_servers,
          "security_protocol": kafka_settings.security_protocol,
          "sasl_mechanism": kafka_settings.sasl_mechanism,
          "sasl_plain_username": kafka_settings.sasl_plain_username,
          "sasl_plain_password": kafka_settings.sasl_plain_password,
          "group_id": kafka_settings.consumer_group_id,
          "value_deserializer": lambda v: json.loads(v.decode('utf-8')),
      }

      self.consumer = AIOKafkaConsumer(*topics, **consumer_config)
      await self.consumer.start()

  async def send_message(self: Self, topic: str, message: dict):

      if not self.producer:
          raise RuntimeError("Producer not initialized. Call start_producer() first.")

      await self.producer.send_and_wait(topic, message)

  async def consume_messages(self: Self) -> AsyncGenerator[dict, None]:

      if not self.producer:
          raise RuntimeError("Consumer not initialized. Call start_consumer() first.")

      async for message in self.consumer:
          yield message.value

  async def close(self: Self):
    
      if self.producer:
          await self.producer.stop()
      if self.consumer:
          await self.consumer.stop()
            
            
kafka_service = KafkaService()