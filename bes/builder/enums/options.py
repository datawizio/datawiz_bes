from enum import Enum


class RenderType(str, Enum):
    table = "table"
    chart = "chart"
    data_frame = "data_frame"


class DataFrameFormatType(str, Enum):
    dict = "dict"
    list = "list"
    split = "split"
    index = "index"
    series = "series"
    records = "records"


class DeltaInterval(str, Enum):
    day = "day"
    week = "week"
    month = "month"
    year = "year"
