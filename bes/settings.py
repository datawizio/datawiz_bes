from typing import List, Optional

from pydantic import BaseSettings, HttpUrl, Field, BaseModel


class OAuth2Settings(BaseModel):
    client_id: Optional[str]
    client_secret: Optional[str]
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

    class Config:
        env_prefix = "bes_"
        env_file = ".env"
        env_file_encoding = "utf-8"


bes_settings: Settings = Settings()
