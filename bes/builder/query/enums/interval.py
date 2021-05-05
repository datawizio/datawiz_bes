from enum import Enum


class Selected(str, Enum):
    date = "date"
    last_update_date = "last_update_date"
    penultimate_update_date = "penultimate_update_date"
    last_7_days = "last_7_days"
    last_30_days = "last_30_days"
    last_180_days = "last_180_days"
    last_365_days = "last_365_days"

    week_begin = "week_begin"
    month_begin = "month_begin"
    season_begin = "season_begin"
    year_begin = "year_begin"

    prev_week = "prev_week"
    prev_month = "prev_month"
    all_time = "all_time"


class PrevSelected(str, Enum):
    prev_date = "prev_date"
    previous = "previous"

    prev_last_week = "prev_last_week"
    prev_last_month = "prev_last_month"
    prev_last_quarter = "prev_last_quarter"
    prev_last_year = "prev_last_year"
