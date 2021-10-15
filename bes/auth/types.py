from typing import Union, Dict, Any

from httpx import Response
from httpx._types import HeaderTypes, QueryParamTypes, RequestData

# Request Types
HeaderTypes = Union[Dict, HeaderTypes]
QueryParamTypes = Union[Dict, QueryParamTypes]
RequestData = Union[str, bytes, RequestData]
RequestResponse = Union[Dict, Response, Any]
