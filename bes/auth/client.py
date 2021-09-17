from typing import Optional, Union

from oauthlib.oauth2 import OAuth2Token
from authlib.integrations.httpx_client import OAuth2Client, AsyncOAuth2Client

from ..settings import bes_settings


class BESOAuth2Mixin:
    """Bes OAuth2 Mixin for set default application credentials"""

    def __init__(self, **kwargs):
        kwargs.setdefault("client_id", bes_settings.oauth2_settings.client_id)
        kwargs.setdefault("client_secret", bes_settings.oauth2_settings.client_secret)
        kwargs.setdefault("auto_refresh_url", bes_settings.oauth2_settings.token_url)
        super(BESOAuth2Mixin, self).__init__(**kwargs)


class BESOAuth2Client(BESOAuth2Mixin, OAuth2Client):
    """Session class for making OAuth2 authenticated requests to BES"""

    def fetch_token(self, url: str = bes_settings.oauth2_settings.token_url, **kwargs) -> OAuth2Token:
        return super(BESOAuth2Mixin, self).fetch_token(url, **kwargs)

    def refresh_token(
            self,
            url: str = bes_settings.oauth2_settings.token_url,
            refresh_token: Optional[str] = None,
            **kwargs
    ) -> OAuth2Token:
        return super(BESOAuth2Mixin, self).refresh_token(url, refresh_token=refresh_token, **kwargs)


class BESAsyncOAuth2Client(BESOAuth2Mixin, AsyncOAuth2Client):
    def fetch_token(self, url: str = bes_settings.oauth2_settings.token_url, **kwargs) -> OAuth2Token:
        return super(BESOAuth2Mixin, self).fetch_token(url, **kwargs)

    def refresh_token(
            self,
            url: str = bes_settings.oauth2_settings.token_url,
            refresh_token: Optional[str] = None,
            **kwargs
    ) -> OAuth2Token:
        return super(BESOAuth2Mixin, self).refresh_token(url, refresh_token=refresh_token, **kwargs)


BESOAuth2ClientTypes = Union[BESOAuth2Client, BESAsyncOAuth2Client]
