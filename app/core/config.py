from pydantic_settings import BaseSettings  # Ahora importado desde pydantic_settings

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
