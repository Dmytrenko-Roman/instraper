from pydantic import BaseSettings


class Settings(BaseSettings):
    instagram_username: str
    instagram_password: str

    class Config:
        env_file = "./.env"


settings = Settings()
