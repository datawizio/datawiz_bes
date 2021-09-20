import logging
from copy import copy
from typing import Optional, Union, Dict, TypeVar

from httpx import Response
from pydantic import validate_arguments

from .client import BESOAuth2Client, BESAsyncOAuth2Client
from .models import Client, User, ClientDefaults
from ..settings import bes_settings

logger = logging.getLogger(__name__)

CLIENT_HEADER = "Client-Id"  # Required header for get info of oauth2client

BESAuthType = TypeVar("BESAuthType", bound="BESAuth")
BESOAuth2ClientType = TypeVar("BESOAuth2ClientType", bound=Union[BESOAuth2Client, BESAsyncOAuth2Client])
RequestResponse = TypeVar("RequestResponse", bound=dict)


class BESAuth:
    def __init__(self, oauth2client: BESOAuth2ClientType, **kwargs):
        self.oauth2client = oauth2client
        self.kwargs = kwargs

        self._user = None
        self._selected_client = None
        self._request_headers = {"Content-Type": "application/json"}

    # OAuth2 Authorization Methods
    @classmethod
    def oauth2(cls, **kwargs) -> BESAuthType:
        return cls(oauth2client=BESOAuth2Client(**kwargs))

    @classmethod
    @validate_arguments
    def access_token(cls, access_token: str) -> BESAuthType:
        return cls(oauth2client=BESOAuth2Client(token={"access_token": access_token}))

    # Request BES Client configuration

    def _set_client_header(self, client: Optional[Client]):
        self._request_headers = self._request_headers.copy()
        if client is None:
            self._request_headers.pop(CLIENT_HEADER, None)
        else:
            self._request_headers[CLIENT_HEADER] = str(client.id)

    def initial(self):
        user_dict = self.get(bes_settings.api_settings.get_url("/api/initial/"))
        # TODO Except when not authorized
        self.user = User(**user_dict)

    def get_defaults(self) -> ClientDefaults:
        data = self.get(url=bes_settings.api_settings.get_url("/api/defaults/"))
        return ClientDefaults(**data)

    @property
    def selected_client(self) -> Optional[Client]:
        return self._selected_client

    @selected_client.setter
    @validate_arguments
    def selected_client(self, client: Optional[Client]):
        self._set_client_header(client)
        # TODO Except when not authorized
        self._selected_client = client
        if self._selected_client is not None:
            self._selected_client.defaults = self.get_defaults()

    @property
    def user(self) -> Optional[User]:
        return self._user

    @user.setter
    @validate_arguments
    def user(self, user: Optional[User]):
        self._user = user
        if self._user is None:
            self.selected_client = None
        else:
            self.selected_client = self.user.clients.first()
        logger.debug("Set user %s", user)

    # Use for different request of oauth2client

    def use(self, client: Optional[Client] = None) -> BESAuthType:
        bes_client = copy(self)
        bes_client.selected_client = client
        return bes_client

    # Request methods
    def _get_request_headers(self, headers: Dict) -> Dict:
        return self._request_headers | headers

    def _check_response(self, response: Response):
        if self.selected_client is not None:
            response_client_id = response.headers.get(CLIENT_HEADER)
            request_client_id = self._request_headers.get(CLIENT_HEADER)
            if request_client_id != response_client_id:
                logger.error("Selected client does not meet the Response client")

    def _request(self, method: str, url: str,
                 data: Optional[Union[str, bytes, Dict]] = None,
                 headers: Optional[Dict] = None,
                 params: Optional[Dict] = None,
                 **kwargs):
        headers = self._get_request_headers(headers or {})
        return self.oauth2client.request(
            method, url=url, data=data, headers=headers, params=params, **kwargs
        )

    def request(
            self, method: str, url: str,
            data: Optional[Union[str, bytes, Dict]] = None,
            headers: Optional[Dict] = None,
            params: Optional[Dict] = None,
            **kwargs
    ) -> RequestResponse:
        # TODO Retry and normalization response
        # TODO Check oauth2client id in header response

        response = self._request(
            method=method, url=url, data=data, headers=headers, params=params, **kwargs
        )
        return response.json()

    def get(self, url: str, params: Optional[Dict] = None, **kwargs) -> RequestResponse:
        return self.request("GET", url, params=params, **kwargs)

    def post(self, url: str, data: Optional[Dict] = None, params: Optional[Dict] = None, **kwargs) -> RequestResponse:
        return self.request("POST", url, data=data, params=params, **kwargs)

    def put(self, url: str, data: Optional[Dict] = None, **kwargs) -> RequestResponse:
        return self.request("PUT", url, data=data, **kwargs)

    def patch(self, url: str, data: Optional[Dict] = None, **kwargs) -> RequestResponse:
        return self.request("PATCH", url, data=data, **kwargs)

    def delete(self, url: str, **kwargs) -> RequestResponse:
        return self.request("DELETE", url, **kwargs)
