from datetime import date
from typing import List, Union, Optional

from pydantic import BaseModel, Field

from .enums.dimension import On, By, Mode
from ...utils import dimension as dimension_utils
from ...utils.generics import ListGenericModel


class Lookups(BaseModel):
    include: Optional[List[Union[int, str, date]]] = Field(min_items=1)
    exclude: Optional[List[Union[int, str, date]]] = Field(min_items=1)
    between: Optional[List[Union[int, str, date]]] = Field(min_items=2, max_items=2)
    equal: Optional[List[Union[int, str, date]]]
    not_equal: Optional[List[Union[int, str, date]]]
    gte: Optional[Union[int, str]]
    gt: Optional[Union[int, str]]
    lte: Optional[Union[int, str]]
    lt: Optional[Union[int, str]]
    negate: bool = False

    @classmethod
    def default(cls):
        return dict()


class Dimension(BaseModel):
    dimension: str
    lookups: Lookups = Field(default_factory=Lookups.default)
    display_fields: List[str] = ["name"]
    force_reindex: Optional[bool]
    on: On = On.row
    by: By = By.id

    @property
    def dimension_display_fields(self) -> List[str]:
        return dimension_utils.dimension_display_fields(self.dimension, self.display_fields)

    class Config:
        use_enum_values = True


class Filters(ListGenericModel[Union[Dimension, "Query"]]):

    @classmethod
    def default(cls):
        return cls()


class Query(BaseModel):
    mode: Mode = Mode.and_
    filters: Filters = Field(default_factory=lambda: Filters.default())
    negate: bool = False


Filters.update_forward_refs()
Query.update_forward_refs()


class GroupBy(ListGenericModel[Dimension]):

    @property
    def columns(self) -> "GroupBy":
        return self.filter(on=On.column)

    @property
    def rows(self) -> "GroupBy":
        return self.filter(on=On.row)

    @classmethod
    def default(cls):
        return cls()
