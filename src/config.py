from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).parent.parent / '.env'


class Config(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    APP_HOST: str
    APP_PORT: int

    @property
    def database_url_psycopg(self):
        return "postgresql+psycopg://{user}:{password}@{host}:{port}/{name}".format(
            user=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            name=self.DB_NAME,
        )

    if env_path.exists():
        model_config = SettingsConfigDict(env_file=env_path)


config = Config()
