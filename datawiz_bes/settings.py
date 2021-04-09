from pydantic import BaseSettings


class Settings(BaseSettings):

    class Config:
        env_file = ".env"
        env_file_encoding = ".env"


datawiz_bes_settings = Settings()
