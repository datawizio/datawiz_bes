from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class PyTestSettings(BaseSettings):
    client_id: Optional[str]
    client_secret: Optional[str]
    username: Optional[str]
    password: Optional[str]
    access_token: Optional[str]

    model_config = SettingsConfigDict(
        env_prefix="BES_PYTEST_",
        env_file=".pytest_env",
        env_file_encoding="utf-8",
    )

    def to_oauth2config(self) -> dict:
        return self.model_dump(include={"client_id", "client_secret"})

    def to_oauth2_auth_basic(self) -> dict:
        return self.model_dump(include={"username", "password"})


settings = PyTestSettings()
