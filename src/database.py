from opensearchpy import AsyncOpenSearch
from config import configs
from exceptions import RAISE_ERROR_EXCEPTION
from es_indexes.messages import create_messages_index_if_not_exists

async def init_es_async_client() -> AsyncOpenSearch:
    es_client = AsyncOpenSearch(
        hosts=[{"host": configs.db_host.get_secret_value(), "port": configs.db_port}]
    )

    if not await es_client.ping():
        raise RAISE_ERROR_EXCEPTION("Cannot connect to OpenSearch")

    await create_messages_index_if_not_exists(es_client=es_client)

    return es_client

