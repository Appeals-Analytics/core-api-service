from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configs(BaseSettings):
    app_port: int

    db_user: SecretStr
    db_password: SecretStr

    db_host: SecretStr
    db_port: int
    db_name: SecretStr

    def get_db_url(self):
        return (
            f"postgresql+asyncpg://{self.db_user.get_secret_value()}:{self.db_password.get_secret_value()}@"
            f"{self.db_host.get_secret_value()}:{self.db_port}/{self.db_name.get_secret_value()}"
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


configs = Configs()
