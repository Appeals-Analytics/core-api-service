from opensearchpy import AsyncOpenSearch
from src.config import configs
from src.exceptions import RAISE_ERROR_EXCEPTION
from src.es_indexes.messages import create_messages_index_if_not_exists

async def init_es_async_client() -> AsyncOpenSearch:
  es_client = AsyncOpenSearch(
    hosts=[configs.db_host],
    http_auth=(configs.db_user, configs.db_password)
    )
  
  if not await es_client.ping():
    raise RAISE_ERROR_EXCEPTION("Cannot to connect to database")
  
  await create_messages_index_if_not_exists(es_client=es_client)
  
  return es_client

