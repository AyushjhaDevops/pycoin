from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "PyCoin"
    app_version: str = "0.1.0"
    environment: str = "development"

    coin_name: str = "PyCoin"
    coin_symbol: str = "PYC"
    coin_decimals: int = Field(default=8, ge=0, le=18)

    consensus_algorithm: str = "proof_of_work"

    api_prefix: str = "/api/v1"


@lru_cache
def get_settings() -> Settings:
    return Settings()
