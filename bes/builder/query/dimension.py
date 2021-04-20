from functools import cached_property
from typing import List, Union

from pydantic import BaseModel, Field

from ..enums.dimension import On
from ...utils import dimension as dimension_utils
from ...utils.generics import ListGenericModel


class Lookups(BaseModel):
    include: List[Union[int, str]] = []
    exclude: List[Union[int, str]] = []

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
    on: On = On.row
    by: str = "id"

    @cached_property
    def dimension_display_fields(self) -> List[str]:
        return dimension_utils.dimension_display_fields(self.dimension, self.display_fields)

    class Config(Dimension.Config):
        keep_untouched = (cached_property,)


class Filters(ListGenericModel[Dimension]):
    pass


class GroupBy(ListGenericModel[DimensionGroupBy]):

    @property
    def columns(self) -> "GroupBy":
        return self.filter(on=On.column)

    @property
    def rows(self) -> "GroupBy":
        return self.filter(on=On.row)
