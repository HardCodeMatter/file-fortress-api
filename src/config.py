from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: str
    APP_HOST: str
    APP_PORT: int
    APP_NAME: str
    APP_VERSION: str
    APP_DESCRIPTION: str

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASS: str
    DATABASE_ECHO: bool
    DATABASE_POOL_SIZE: int

    @property
    def DATABASE_URL(self) -> str:
        return f'postgresql+asyncpg://{self.DATABASE_HOST}:{self.DATABASE_PORT}@{self.DATABASE_USER}:{self.DATABASE_PASS}/{self.DATABASE_NAME}?async_fallback=True'

    model_config = SettingsConfigDict(
        env_file='.env',
    )


settings = Settings()
