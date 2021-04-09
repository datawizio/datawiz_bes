from typing import Union

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
    "Dimension",
    "DimensionGroupBy",
    "GroupBy",
    "Filters",
    "DateRange",
    "PrevDateRange",
    "Metric",
    "Aggregate",
    "Options",
    "TableRenderOptions",
    "ChartRenderOptions",
    "DataFrameRenderOptions",
    "BuilderQuery",
)


class BuilderQuery(BaseModel):
    date_range: DateRange = Field(default_factory=DateRange.default)
    prev_date_range: PrevDateRange = Field(default_factory=PrevDateRange.default)

    group_by: GroupBy = Field(default_factory=list)
    aggregate: Aggregate = Field(default_factory=list)
    filters: Filters = Field(default_factory=list)

    options: Options = Field(default_factory=dict)
    render_options: Union[
        RenderOptions,
        TableRenderOptions,
        ChartRenderOptions,
        DataFrameRenderOptions
    ] = Field(default_factory=TableRenderOptions.default)
