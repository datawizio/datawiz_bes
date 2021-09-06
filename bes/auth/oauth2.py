from typing import Optional

from oauthlib.oauth2 import LegacyApplicationClient, OAuth2Token
from pydantic import validate_arguments
from requests import Response
from requests_oauthlib import OAuth2Session

from .models import User
from ..settings import bes_settings

CLIENT_HEADER = "Client-Id"  # Required header for get info of client


class BESAuth:

    @validate_arguments
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password
        self._user = None

        self._auth_session = self._get_auth_session()
        self._auth_session_fetch_token()

        self.initial()

    def initial(self):
        url_initial = bes_settings.oauth2_settings.get_url("/api/initial/")
        response = self.get(url=url_initial)
        if response.status_code != 200:
            # TODO Raise Error
            return
        data = response.json()
        self._user = User(**data)

    @property
    def user(self) -> Optional[User]:
        return self._user

    def _get_auth_session(self) -> OAuth2Session:
        return OAuth2Session(
            client=LegacyApplicationClient(client_id=bes_settings.oauth2_settings.client_id),
            scope=bes_settings.oauth2_settings.scope,
            token_updater=self._auth_session_token_updater,
            auto_refresh_url=bes_settings.oauth2_settings.token_url,
            auto_refresh_kwargs={
                "client_id": bes_settings.oauth2_settings.client_id,
                "client_secret": bes_settings.oauth2_settings.client_secret,
            },
        )

    def _auth_session_fetch_token(self) -> OAuth2Token:
        token = self._auth_session.fetch_token(
            token_url=bes_settings.oauth2_settings.token_url,
            username=self._username,
            password=self._password,
            client_id=bes_settings.oauth2_settings.client_id,
            client_secret=bes_settings.oauth2_settings.client_secret,
        )
        return token

    def _auth_session_token_updater(self, token: OAuth2Token):
        pass  # Save token

    def _get_headers(self, headers: Optional[dict] = None) -> dict:
        headers = headers or {}
        if self._client:
            headers.setdefault(CLIENT_HEADER, str(self._client.id))
        return headers

    def post(self, url: str, data=None, json=None, params=None, headers=None, **kwargs) -> Response:
        headers = self._get_headers(headers)
        return self._auth_session.post(url=url, data=data, json=json, params=params, headers=headers, **kwargs)

    def get(self, url: str, data=None, params=None, headers=None, **kwargs) -> Response:
        headers = self._get_headers(headers)
        return self._auth_session.get(url=url, data=data, params=params, headers=headers, **kwargs)
