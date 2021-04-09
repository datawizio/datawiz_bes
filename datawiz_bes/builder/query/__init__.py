from typing import Union, Type

from pydantic import BaseModel, Field

from .dimension import Dimension, DimensionGroupBy, GroupBy, Filters
from .interval import DateRange, PrevDateRange
from .metric import Metric, Aggregate
from .options import (
    Options,
    RenderOptions,
    TableRenderOptions,
    ChartRenderOptions,
    DataFrameRenderOptions
)

__all__ = (
    "BuilderQuery",
    "Dimension",
    "DimensionGroupBy",
    "GroupBy",
    "Metric",
    "DateRange",
    "PrevDateRange",
    "Options",
    "TableRenderOptions",
    "ChartRenderOptions",
    "DataFrameRenderOptions",
)


class BuilderQuery(BaseModel):
    date_range: DateRange = Field(default_factory=DateRange.default)
    prev_date_range: PrevDateRange = Field(default_factory=PrevDateRange.default)

    group_by: GroupBy = []
    aggregate: Aggregate = []
    filters: Filters = []

    options: Options = Field(default_factory=dict)
    render_options: Union[
        RenderOptions,
        TableRenderOptions,
        ChartRenderOptions,
        DataFrameRenderOptions
    ] = Field(default_factory=TableRenderOptions.default)
