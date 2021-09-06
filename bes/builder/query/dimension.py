from functools import cached_property
from typing import List, Union, Optional

from pydantic import BaseModel, Field

from .enums.dimension import On
from ...utils import dimension as dimension_utils
from ...utils.generics import ListGenericModel


class Lookups(BaseModel):
    include: Optional[List[Union[int, str]]] = Field(min_items=1)
    exclude: Optional[List[Union[int, str]]] = Field(min_items=1)
    between: Optional[List[Union[int, str]]] = Field(min_items=2, max_items=2)
    equal: Optional[List[Union[int, str]]]
    not_equal: Optional[List[Union[int, str]]]
    negate: bool = False

    @classmethod
    def default(cls):
        return dict()


class Dimension(BaseModel):
    dimension: str
    lookups: Lookups = Field(default_factory=Lookups.default)

    class Config:
        use_enum_values = True


class DimensionGroupBy(Dimension):
    display_fields: List[str] = ["name"]
    force_reindex: Optional[bool]
    on: On = On.row
    by: str = "id"

    @cached_property
    def dimension_display_fields(self) -> List[str]:
        return dimension_utils.dimension_display_fields(self.dimension, self.display_fields)

    class Config(Dimension.Config):
        keep_untouched = (cached_property,)


class Filters(ListGenericModel[Dimension]):

    @classmethod
    def default(cls):
        return cls()


class GroupBy(ListGenericModel[DimensionGroupBy]):

    @property
    def columns(self) -> "GroupBy":
        return self.filter(on=On.column)

    @property
    def rows(self) -> "GroupBy":
        return self.filter(on=On.row)

    @classmethod
    def default(cls):
        return cls()
