from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    # 개발용 SQLite (나중에 PostgreSQL로만 URL 바꾸면 됨)
    DATABASE_URL: str = "sqlite+aiosqlite:///./dev.db"
    APP_ENV: str = "dev"


settings = Settings()