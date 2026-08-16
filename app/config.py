from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
    )


settings = DbSettings()
print(settings.POSTGRES_USER, settings.POSTGRES_PASSWORD)
