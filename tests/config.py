from typing import Optional

from pydantic.v1 import BaseSettings


class PyTestSettings(BaseSettings):
    client_id: Optional[str]
    client_secret: Optional[str]
    username: Optional[str]
    password: Optional[str]
    access_token: Optional[str]

    class Config:
        env_prefix = "BES_PYTEST_"
        env_file = ".pytest_env"
        env_file_encoding = "utf-8"

    def to_oauth2config(self) -> dict:
        return self.dict(include={"client_id", "client_secret"})

    def to_oauth2_auth_basic(self) -> dict:
        return self.dict(include={"username", "password"})


settings = PyTestSettings()
