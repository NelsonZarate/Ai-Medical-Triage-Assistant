from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    OPENAI_API_KEY: str

    ENVIRONMENT: str
    PORT: int
    
    database_driver: str
    database_username: str
    database_password: str
    database_host: str
    database_port: int
    database_name: str

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    """
    Função para obter as configurações, com cache para performance.
    """
    return Settings()

settings = get_settings()