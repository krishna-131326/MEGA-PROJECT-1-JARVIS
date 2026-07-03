from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    news_api_key: str = ""
    grok_api_key: str = ""
    grok_model: str = "grok-beta"
    music_config_path: str = "music/config.json"
    environment: str = "development"
    log_level: str = "INFO"
    memory_max_history: int = 20

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
