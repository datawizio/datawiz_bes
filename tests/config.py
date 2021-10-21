import os
from typing import Optional

from pydantic import BaseSettings


class PyTestSettings(BaseSettings):
    client_id: Optional[str] = os.getenv("BES_PYTEST_CLIENT_ID")
    client_secret: Optional[str] = os.getenv("BES_PYTEST_CLIENT_SECRET")
    username: Optional[str] = os.getenv("BES_PYTEST_USERNAME")
    password: Optional[str] = os.getenv("BES_PYTEST_PASSWORD")
    access_token: Optional[str] = os.getenv("BES_PYTEST_ACCESS_TOKEN")

    class Config:
        env_prefix = "BES_PYTEST_"
        env_file = ".pytest_env"
        env_file_encoding = "utf-8"

    def to_oauth2config(self) -> dict:
        return self.dict(include={"client_id", "client_secret"})

    def to_oauth2_auth_basic(self) -> dict:
        return self.dict(include={"username", "password"})


settings = PyTestSettings()
