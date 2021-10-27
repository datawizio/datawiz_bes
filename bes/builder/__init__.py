from typing import Any

from httpx import QueryParams

from .query import BuilderQuery
from ..auth import BESAuth
from ..auth.types import QueryParamTypes
from ..settings import bes_settings

__all__ = (
    "BuilderQuery",
    "BESBuilder",
)


class BESBuilder:

    def __init__(self, query: BuilderQuery, auth: BESAuth):
        self.query = query
        self.auth = auth

        self.query_params = QueryParams({"page_size": 100})

    def _query_params_set(self, key: str, value: Any):
        self.query_params = self.query_params.set(key, value)

    def ordering(self, *ordering_fields: str) -> "BESBuilder":
        """Set ordering values"""
        self._query_params_set("ordering", ",".join(ordering_fields))
        return self

    def search(self, value: str) -> "BESBuilder":
        """Set search value"""
        self._query_params_set("search", value)
        return self

    def page_size(self, page_size: int) -> "BESBuilder":
        """Set page size for server response"""
        self._query_params_set("page_size", page_size)
        return self

    def fetch_data(self, query_params: QueryParamTypes = None):
        url = bes_settings.api.get_api_url("/builder/create-table/")
        data = self.query.to_json()
        query_params = self.query_params.merge(query_params or {})
        res = self.auth.post(url=url, data=data, headers={"Content-Type": "application/json"}, params=query_params)
        return res

    def fetch_all(self):
        return self.fetch_data(query_params={"page_size": "full"})
