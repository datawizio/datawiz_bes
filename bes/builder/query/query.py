from pydantic import BaseModel, Field

from .enums import Mode


class Query(BaseModel):
    mode: Mode = Mode.and_
    filters: "Filters" = Field(default_factory=lambda: Filters.default())
    negate: bool = False


from .dimension import Filters

Query.update_forward_refs()
