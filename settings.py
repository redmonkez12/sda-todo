from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str
    DB_PASSWORD: str
    DB_USERNAME: str
    DB_HOST: str
    DB_PORT: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"
