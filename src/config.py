from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Configs(BaseSettings):
  
  app_port: int
  database_url: SecretStr
  
  model_config = SettingsConfigDict(env_file=".env")
  
  
configs = Configs()