from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class OAuth2Settings(BaseModel):
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    host: HttpUrl = "https://bes.datawiz.io"
    authorize_path: str = "/o/authorize/"
    token_path: str = "/o/token/"
    scope: List[str] = ["write", "read"]

    def get_url(self, path: str) -> str:
        return "{host}{path}".format(host=self.host, path=path)

    @property
    def authorize_url(self) -> str:
        return self.get_url(path=self.authorize_path)

    @property
    def token_url(self) -> str:
        return self.get_url(path=self.token_path)

    @classmethod
    def default(cls):
        return cls()


class ApiSettings(BaseModel):
    host: HttpUrl = "https://api-new.datawiz.io"
    api_path: str = "/api"

    def get_url(self, path: str) -> str:
        return "{host}{path}".format(host=self.host, path=path)

    def get_api_url(self, path: str) -> str:
        return "{url}{path}".format(url=self.get_url(self.api_path), path=path)

    @classmethod
    def default(cls):
        return cls()


class Settings(BaseSettings):
    oauth2: OAuth2Settings = Field(default_factory=OAuth2Settings.default)
    api: ApiSettings = Field(default_factory=ApiSettings.default)

    host: Optional[HttpUrl] = Field(default=None, exclude=True)
    oauth_host: Optional[HttpUrl] = Field(default=None, exclude=True)

    model_config = SettingsConfigDict(
        env_prefix="bes_",
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    @model_validator(mode="after")
    def _apply_legacy_hosts(self):
        updates = {}

        if self.host is not None and "host" not in self.api.model_fields_set:
            updates["api"] = self.api.model_copy(update={"host": self.host})

        if self.oauth_host is not None and "host" not in self.oauth2.model_fields_set:
            updates["oauth2"] = self.oauth2.model_copy(update={"host": self.oauth_host})

        return self.model_copy(update=updates) if updates else self


bes_settings: Settings = Settings()
