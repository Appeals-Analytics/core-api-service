from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class KafkaSettings(BaseSettings):
    bootstrap_servers: SecretStr
    security_protocol: SecretStr
    sasl_mechanism: str = SecretStr
    sasl_plain_username: SecretStr
    sasl_plain_password: SecretStr

    consumer_group_id: str

    topic_in: str
    topic_out: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


kafka_settings = KafkaSettings()
