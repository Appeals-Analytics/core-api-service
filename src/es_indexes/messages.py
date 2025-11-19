from opensearchpy import AsyncOpenSearch

INDEX_NAME = "messages"

async def create_messages_index_if_not_exists(*, es_client: AsyncOpenSearch) -> None:

    if await es_client.indices.exists(index=INDEX_NAME):
        print(f"Index '{INDEX_NAME}' already exists.")
        return

    print(f"Index '{INDEX_NAME}' not found. Creating...")

    mapping = {
      "settings": {
        "analysis": {
          "analyzer": {
            "default_russian": {
              "type": "custom",
              "tokenizer": "standard",
              "filter": ["lowercase", "russian_stop", "russian_stemmer"]
            }
          },
          "filter": {
            "russian_stop": {"type": "stop", "stopwords": "_russian_"},
            "russian_stemmer": {"type": "stemmer", "language": "russian"}
          }
        }
      },
      "mappings": {
        "properties": {
          "id": {"type": "keyword"},
          "external_id": {"type": "keyword"},
          "created_at": {"type": "date"},
          "source": {"type": "keyword"},
          "user_id": {"type": "keyword"},
          "event_date": {"type": "date"},
          "text": {"type": "text", "analyzer": "default_russian"},
          "cleaned_text": {"type": "text", "analyzer": "default_russian"},
          "language": {
            "type": "object",
            "properties": {
              "code": {"type": "keyword"},
              "score": {"type": "float"}
            }
          },
          "sentiment": {
            "type": "object",
            "properties": {
              "label": {"type": "keyword"},
              "score": {"type": "float"}
            }
          },
          "emotion": {
            "type": "object",
            "properties": {
              "label": {"type": "keyword"},
              "score": {"type": "float"}
            }
          },
          "level_1": {"type": "keyword"},
          "level_2": {"type": "keyword"}
        }
      }
    }

    try:
        await es_client.indices.create(index=INDEX_NAME, body=mapping)
        print(f"Index '{INDEX_NAME}' created successfully.")
    except Exception as e:
        print(f"Error creating index '{INDEX_NAME}': {e}")
        raise