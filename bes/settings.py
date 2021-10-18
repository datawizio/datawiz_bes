from typing import List

from pydantic import BaseSettings, BaseModel, HttpUrl, Field


class OAuth2Settings(BaseModel):
    client_id: str = "R6lRcOFoUtqNrXiCNtAo5yMIcInUtEKooNP4JCcI"
    client_secret: str = "md9PZH9IwgaQFdL3jTE52tbdyI7brkZx2rS6hPs0oUbmLGmliMD7DM6" \
                         "qIJ9zsOaoEZueGSvq19BVelc1TeXPVJeni3LNsGT1SCQP5EVHR28JLRdfDzRJejVQ7K9jzbNs"
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


class ApiSettings(BaseSettings):
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
    oauth2_settings: OAuth2Settings = Field(default_factory=OAuth2Settings.default)
    api_settings: ApiSettings = Field(default_factory=ApiSettings.default)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


bes_settings: Settings = Settings()
