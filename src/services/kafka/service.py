import json
from typing import AsyncGenerator, Optional, Self
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer, TopicPartition
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from aiokafka.errors import TopicAlreadyExistsError
from src.database.database import AsyncSessionLocal
from src.api.message.service import MessageService
from src.api.message.schemas import MessageCreate

from src.services import kafka_settings


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

  async def consume_messages(self: Self) -> AsyncGenerator[dict, None]:
    if not self.consumer:
      raise RuntimeError("Consumer not initialized. Call start_consumer() first.")

    async for message in self.consumer:
      yield message.value

  async def consume_and_save_messages(self: Self):
    """Consume messages and save them to the database"""
    if not self.consumer:
      raise RuntimeError("Consumer not initialized. Call start_consumer() first.")

    async for message in self.consumer:
      if message.topic != kafka_settings.topic_in:
        continue

      tp = TopicPartition(message.topic, message.partition)
      try:
        message_data = json.loads(message.value)
        async with AsyncSessionLocal() as session:
          msg_create = MessageCreate(**message_data)
          print(message_data)
          await MessageService.create_message(session, msg_create)

          await self.consumer.commit({tp: message.offset + 1})
      except Exception as e:
        print(f"Error processing Kafka message: {e}")

  async def close(self: Self):
    if self.producer:
      await self.producer.stop()
    if self.consumer:
      await self.consumer.stop()
    if self.admin:
      await self.admin.close()


kafka_service = KafkaService()
