from typing import Union

from pydantic import BaseModel, Field

from .dimension import Dimension, DimensionGroupBy, GroupBy, Filters, Lookups
from .interval import DateRange, PrevDateRange, TimeRange
from .metric import Metric, Aggregate, MetricFilter, MetricFormat
from .options import (
    Options,
    RenderOptions,
    TableRenderOptions,
    ChartRenderOptions,
    DataFrameRenderOptions
)

__all__ = (
    "DateRange",
    "PrevDateRange",
    "TimeRange",
    "Dimension",
    "DimensionGroupBy",
    "Lookups",
    "GroupBy",
    "Filters",
    "DateRange",
    "PrevDateRange",
    "Metric",
    "MetricFilter",
    "MetricFormat",
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
    time_range: TimeRange = Field(default_factory=TimeRange.default)

    aggregate: Aggregate = Field(default_factory=Aggregate.default)
    group_by: GroupBy = Field(default_factory=GroupBy.default)
    filters: Filters = Field(default_factory=Filters.default)

    options: Options = Field(default_factory=Options.default)
    render_options: Union[
        RenderOptions,
        TableRenderOptions,
        ChartRenderOptions,
        DataFrameRenderOptions
    ] = Field(default_factory=TableRenderOptions.default)
