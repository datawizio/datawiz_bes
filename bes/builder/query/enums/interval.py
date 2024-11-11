from enum import Enum


class Selected(str, Enum):
    date = "date"
    last_update_date = "last_update_date"
    penultimate_update_date = "penultimate_update_date"
    last_7_days = "last_7_days"
    last_30_days = "last_30_days"
    last_90_days = "last_90_days"
    last_180_days = "last_180_days"
    last_365_days = "last_365_days"

    week_begin = "week_begin"
    month_begin = "month_begin"
    quarter_begin = "quarter_begin"
    year_begin = "year_begin"

    prev_week = "prev_week"
    prev_month = "prev_month"
    prev_quarter = "prev_quarter"
    prev_year = "prev_year"

    current_day = "current_day"
    current_week = "current_week"
    current_month = "current_month"
    current_quarter = "current_quarter"
    current_year = "current_year"

    all_time = "all_time"


class PrevSelected(str, Enum):
    prev_date = "prev_date"
    previous = "previous"

    prev_last_week = "prev_last_week"
    prev_last_month = "prev_last_month"
    prev_last_quarter = "prev_last_quarter"
    prev_last_year = "prev_last_year"

    same_weekday_prev_year = "same_weekday_prev_year"
