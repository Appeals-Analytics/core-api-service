from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configs(BaseSettings):
  app_port: int

  db_user: SecretStr = "default"
  db_password: SecretStr = "password"

  db_host: SecretStr = "localhost"
  db_port: int = 9000
  db_name: SecretStr = "analytics"

  kafka_batch_size: int = 1000
  kafka_flush_interval: int = 60

  def get_db_url(self):
    return (
      f"clickhouse+asynch://{self.db_user.get_secret_value()}:{self.db_password.get_secret_value()}@"
      f"{self.db_host.get_secret_value()}:{self.db_port}/{self.db_name.get_secret_value()}"
    )

  model_config = SettingsConfigDict(env_file=".env", extra="ignore")


configs = Configs()
