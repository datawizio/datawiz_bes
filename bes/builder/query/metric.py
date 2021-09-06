from typing import List, Union, Optional

from pydantic import BaseModel

from .enums.metric import Condition, DType
from ...utils.generics import ListGenericModel


class MetricFilter(BaseModel):
    condition: Condition
    value: Union[int, float]

    class Config:
        use_enum_values = True


class MetricFormat(BaseModel):
    dtype: DType = DType.number
    decimals: Optional[int]

    class Config:
        use_enum_values = True


class Metric(BaseModel):
    metric: str
    title: Optional[str]
    dformat: Optional[MetricFormat]
    filters: Optional[List[MetricFilter]]


class Aggregate(ListGenericModel[Metric]):

    @classmethod
    def default(cls):
        return cls()
