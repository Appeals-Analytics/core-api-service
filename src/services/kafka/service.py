import json
from typing import AsyncGenerator, Optional, Self
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer, TopicPartition
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from aiokafka.errors import TopicAlreadyExistsError
from src.database.database import AsyncSessionLocal
from src.api.message.service import MessageService
from src.api.message.schemas import MessageCreate

from src.services import kafka_settings
from src.app.config import configs
import asyncio
import time


class KafkaService:
  def __init__(self: Self):
    self.producer: Optional[AIOKafkaProducer] = None
    self.consumer: Optional[AIOKafkaConsumer] = None
    self.admin: Optional[AIOKafkaAdminClient] = None

  def _get_connection_config(self: Self) -> dict:
    """Get common connection config for Kafka clients"""
    return {
      "bootstrap_servers": kafka_settings.bootstrap_servers.get_secret_value(),
      "security_protocol": kafka_settings.security_protocol.get_secret_value(),
      "sasl_mechanism": kafka_settings.sasl_mechanism,
      "sasl_plain_username": kafka_settings.sasl_plain_username.get_secret_value(),
      "sasl_plain_password": kafka_settings.sasl_plain_password.get_secret_value(),
    }

  async def _ensure_admin(self: Self):
    """Ensure admin client is started"""
    if not self.admin:
      self.admin = AIOKafkaAdminClient(**self._get_connection_config())
      await self.admin.start()

  async def ensure_topic_exists(
    self: Self,
    topic: str,
    num_partitions: int = 3,
    replication_factor: int = 1,
  ):
    """Create topic if it doesn't exist"""
    await self._ensure_admin()
    try:
      existing_topics = await self.admin.list_topics()
      if topic not in existing_topics:
        new_topic = NewTopic(
          name=topic,
          num_partitions=num_partitions,
          replication_factor=replication_factor,
        )
        await self.admin.create_topics([new_topic])
        print(f"Topic '{topic}' created successfully")
      else:
        print(f"Topic '{topic}' already exists")
    except TopicAlreadyExistsError:
      print(f"Topic '{topic}' already exists")
    except Exception as e:
      print(f"Error creating topic '{topic}': {e}")
    finally:
      await self.admin.close()

  async def start_producer(self: Self):
    producer_config = {
      **self._get_connection_config(),
      "value_serializer": lambda v: json.dumps(v).encode("utf-8"),
    }

    self.producer = AIOKafkaProducer(**producer_config)
    await self.producer.start()

  async def start_consumer(self: Self, topics: list[str]):
    for topic in topics:
      await self.ensure_topic_exists(topic)

    consumer_config = {
      **self._get_connection_config(),
      "group_id": kafka_settings.consumer_group_id,
      "auto_offset_reset": "earliest",
      "enable_auto_commit": True,
      "value_deserializer": lambda v: json.loads(v.decode("utf-8")),
    }

    self.consumer = AIOKafkaConsumer(*topics, **consumer_config)
    await self.consumer.start()

  async def send_message(self: Self, topic: str, message: dict):
    if not self.producer:
      raise RuntimeError("Producer not initialized. Call start_producer() first.")

    await self.producer.send_and_wait(topic, message)

  async def send_messages(self: Self, topic: str, messages: list[str]):
    """Send multiple messages to Kafka efficiently"""
    if not self.producer:
      raise RuntimeError("Producer not initialized. Call start_producer() first.")

    for message in messages:
      # If message is already a string (JSON), we might want to bypass serializer or pass it as is if serializer handles it.
      # But serializer is fixed to json.dumps.
      # If we pass a dict, it works.
      # If FilesService passes strings, we should probably parse them back or change FilesService to pass dicts.
      await self.producer.send(topic, message)

    await self.producer.flush()

  async def consume_messages(self: Self) -> AsyncGenerator[dict, None]:
    if not self.consumer:
      raise RuntimeError("Consumer not initialized. Call start_consumer() first.")

    async for message in self.consumer:
      yield message.value

  async def consume_and_save_messages(self: Self):
    """Consume messages and save them to the database in batches"""
    if not self.consumer:
      raise RuntimeError("Consumer not initialized. Call start_consumer() first.")

    batch = []
    last_flush_time = time.time()

    while True:
      try:
        result = await self.consumer.getmany(timeout_ms=1000, max_records=configs.kafka_batch_size)

        for tp, messages in result.items():
          for message in messages:
            if message.topic != kafka_settings.topic_in:
              continue

            try:
              message_data = json.loads(message.value)
              validated_msg = MessageCreate(**message_data)

              msg_dict = validated_msg.model_dump()

              batch.append(msg_dict)
            except Exception as e:
              print(f"Error parsing/validating Kafka message: {e}")

        current_time = time.time()
        is_batch_full = len(batch) >= configs.kafka_batch_size
        is_time_to_flush = (current_time - last_flush_time) >= configs.kafka_flush_interval

        if batch and (is_batch_full or is_time_to_flush):
          print(
            f"Flushing {len(batch)} messages to ClickHouse. trigger: {'batch_full' if is_batch_full else 'timeout'}"
          )
          try:
            async with AsyncSessionLocal() as session:
              await MessageService.create_messages_batch(session, batch)

            await self.consumer.commit()

            batch = []
            last_flush_time = current_time
            print("Flush successful.")
          except Exception as e:
            print(f"Error saving batch to ClickHouse: {e}")
            await asyncio.sleep(10)
        elif not batch:
          pass
        await asyncio.sleep(10)

      except Exception as e:
        print(f"Error in consumer loop: {e}")
        await asyncio.sleep(1)

  async def close(self: Self):
    if self.producer:
      await self.producer.stop()
    if self.consumer:
      await self.consumer.stop()
    if self.admin:
      await self.admin.close()


kafka_service = KafkaService()
