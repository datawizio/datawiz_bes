from datetime import date, time
from typing import Optional, Dict

from pydantic.v1 import BaseModel, root_validator

from .enums.interval import Selected, PrevSelected


class DateRange(BaseModel):
    selected: Selected = Selected.last_update_date
    date_from: Optional[date]
    date_to: Optional[date]

    @root_validator()
    def date_range_require(cls, values: Dict) -> Dict:
        if values.get("selected") == Selected.date:
            assert (
                values.get("date_from") is not None and values.get("date_to") is not None
            ), f"date_from, date_to is required for '{Selected.date}'"
        return values

    @classmethod
    def default(cls):
        return cls()

    class Config:
        use_enum_values = True


class PrevDateRange(DateRange):
    selected: PrevSelected = PrevSelected.previous

    @root_validator()
    def date_range_require(cls, values: Dict) -> Dict:
        if values.get("selected") == PrevSelected.prev_date:
            assert (
                values.get("date_from") is not None and values.get("date_to") is not None
            ), f"date_from, date_to is required for '{PrevSelected.prev_date}'"
        return values


class TimeRange(BaseModel):
    time_from: time = time(0, 0, 0)
    time_to: time = time(23, 59, 59)

    @classmethod
    def default(cls):
        return cls()
