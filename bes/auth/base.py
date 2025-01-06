import json
from copy import copy
from logging import getLogger
from typing import Optional, Dict, Literal, Callable, Union, Tuple

from authlib.integrations.base_client import OAuthError
from httpx import Response, codes
from pydantic.v1 import validate_arguments
from tenacity import retry, retry_if_exception_type, stop_after_attempt

from . import errors
from .client import BESOAuth2Client
from .constants import CLIENT_ID_HEADER
from .models import Client, User, ClientDefaults
from .types import RequestData, RequestResponse, QueryParamTypes, HeaderTypes
from ..settings import bes_settings

__all__ = (
    "BESAuth",
)

logger = getLogger(__name__)


class BESAuth:
    def __init__(self, oauth2client: "BESOAuth2Client"):
        self.oauth2client = oauth2client

        self._user = None
        self._selected_client = None
        self._request_headers = {}

    # OAuth2 Authorization Methods
    @classmethod
    def oauth2(cls, **kwargs) -> "BESAuth":
        return cls(oauth2client=BESOAuth2Client(**kwargs))

    @classmethod
    def access_token(cls, access_token: str) -> "BESAuth":
        return cls(oauth2client=BESOAuth2Client(token={"access_token": access_token}))

    # Request BES Client configuration

    def _set_client_header(self, client: Optional[Client]):
        self._request_headers = self._request_headers.copy()
        if client is None:
            self._request_headers.pop(CLIENT_ID_HEADER, None)
        else:
            self._request_headers[CLIENT_ID_HEADER] = str(client.id)

    def initial(self):
        """Initial information about authorization user"""
        user_dict = self.get(bes_settings.api.get_url("/api/initial/"))
        self.user = User(**user_dict)

    def get_client_defaults(self) -> ClientDefaults:
        """Get default information about client."""
        data = self.get(url=bes_settings.api.get_url("/api/defaults/"))
        return ClientDefaults(**data)

    @property
    def selected_client(self) -> Optional[Client]:
        """Processing and getting data from server of the selected client.
        The client is identified by the key `Client-Id` in the headers.
        """
        return self._selected_client

    @selected_client.setter
    @validate_arguments
    def selected_client(self, client: Optional[Client]):
        self._set_client_header(client)
        self._selected_client = client
        if self._selected_client is not None:
            self._selected_client.defaults = self.get_client_defaults()
        logger.debug("Selected client: Client(%s)", self.selected_client)

    @property
    def user(self) -> Optional[User]:
        """User of authorization session."""
        return self._user

    @user.setter
    @validate_arguments
    def user(self, user: Optional[User]):
        """Set user of authorization session and selected client."""
        self._user = user
        if self._user is None:
            self.selected_client = None
        else:
            self.selected_client = self.user.clients.first()
        logger.debug("Set user User(%s)", user)

    # Use for different request of oauth2client

    def use(self, client: Optional[Client] = None) -> "BESAuth":
        bes_client = copy(self)
        bes_client.selected_client = client
        return bes_client

    # Process request methods
    def _get_request_headers(self, headers: HeaderTypes) -> Dict:
        request_headers = self._request_headers.copy()
        request_headers.update(headers)
        return request_headers

    @staticmethod
    def _format_request_data(data: RequestData, headers: Dict) -> Tuple[RequestData, Dict]:
        if isinstance(data, dict):
            headers.setdefault("Content-Type", "application/json")
            data = json.dumps(data)
        return data, headers

    def _check_response(self, response: Response):
        if self.selected_client is not None:
            response_client_id = response.headers.get(CLIENT_ID_HEADER)
            request_client_id = self._request_headers.get(CLIENT_ID_HEADER)
            if response_client_id is not None and request_client_id != response_client_id:
                # Bes has no client_id in headers
                raise errors.BESSelectedClientError(
                    request_client_id=request_client_id,
                    response_client_id=response_client_id
                )

        if response.is_success:
            return  # Is success response from server

        if response.status_code == codes.bad_request:
            raise errors.BESBadRequestError(response=response)

        if response.is_server_error:
            raise errors.BESServerError(response=response)

    @retry(retry=retry_if_exception_type((OAuthError, errors.BESRetryError)), stop=stop_after_attempt(2))
    def _request(
            self,
            method: str,
            url: str,
            data: RequestData = None,
            headers: HeaderTypes = None,
            params: QueryParamTypes = None,
            **kwargs
    ):
        headers = self._get_request_headers(headers or {})
        data, headers = self._format_request_data(data, headers)
        response = self.oauth2client.request(method, url=url, data=data, headers=headers, params=params, **kwargs)
        self._check_response(response)
        return response

    def request(
            self,
            method: str,
            url: str,
            data: RequestData = None,
            headers: HeaderTypes = None,
            params: QueryParamTypes = None,
            response_type: Optional[Union[Literal["dict"], Callable]] = "dict",
            **kwargs
    ) -> RequestResponse:
        response = self._request(method=method, url=url, data=data, headers=headers, params=params, **kwargs)
        # TODO different content type
        if response_type == "dict":
            return response.json()

        if callable(response_type):
            return response_type(response)

        return response

    # Request methods

    def get(self, url: str, params: QueryParamTypes = None, **kwargs) -> RequestResponse:
        return self.request("GET", url, params=params, **kwargs)

    def post(self, url: str, data: RequestData = None, params: QueryParamTypes = None, **kwargs) -> RequestResponse:
        return self.request("POST", url, data=data, params=params, **kwargs)

    def put(self, url: str, data: RequestData = None, **kwargs) -> RequestResponse:
        return self.request("PUT", url, data=data, **kwargs)

    def patch(self, url: str, data: RequestData = None, **kwargs) -> RequestResponse:
        return self.request("PATCH", url, data=data, **kwargs)

    def delete(self, url: str, **kwargs) -> RequestResponse:
        return self.request("DELETE", url, **kwargs)
