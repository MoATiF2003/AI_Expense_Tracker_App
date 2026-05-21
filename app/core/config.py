from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    DEBUG: bool

    API_V1_PREFIX: str

    DATABASE_URL: str

    GROQ_API_KEY: str

    class Config:
        env_file = ".env"

settings = Setting()