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
    minute = "minute"
    minute10 = "minute10"
    minute30 = "minute30"
    hour = "hour"
    hour2 = "hour2"
    hour3 = "hour3"
    hour4 = "hour4"
    week_day = "week_day"
    week = "week"
    month = "month"
    quarter = "quarter"
    year = "year"
    month_year = "month_year"
    day_month_year = "day_month_year"
