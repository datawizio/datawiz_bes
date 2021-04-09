from typing import List, Union, Optional

from pydantic import BaseModel, Field

from ..enums.dimension import On
from ...utils.generics import ListGenericModel


class Lookups(BaseModel):
    include: Optional[List[Union[int, str]]]
    exclude: Optional[List[Union[int, str]]]

    @classmethod
    def default(cls):
        return dict()


class Dimension(BaseModel):
    dimension: str
    lookups: Lookups = Field(default_factory=Lookups.default)

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True


class DimensionGroupBy(Dimension):
    display_fields: List[str] = ["name"]
    on: On = On.row
    by: str = "id"


class Filters(ListGenericModel[Dimension]):
    pass


class GroupBy(ListGenericModel[DimensionGroupBy]):

    @property
    def columns(self) -> "GroupBy":
        return self.filter(on=On.column)

    @property
    def rows(self) -> "GroupBy":
        return self.filter(on=On.row)
