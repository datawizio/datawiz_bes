from datetime import date
from typing import Optional

from pydantic import BaseModel, root_validator

from .enums.interval import Selected, PrevSelected


class DateRange(BaseModel):
    selected: Selected = Selected.last_update_date
    date_from: Optional[date]
    date_to: Optional[date]

    @root_validator()
    def date_range_require(cls, values):
        if values["selected"] == Selected.date:
            assert values["date_from"] is not None and values["date_to"] is not None, \
                f"date_from, date_to is required for '{Selected.date}'"
        return values

    @classmethod
    def default(cls):
        return cls()

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True


class PrevDateRange(DateRange):
    selected: PrevSelected = PrevSelected.previous

    @root_validator()
    def date_range_require(cls, values):
        if values["selected"] == Selected.date:
            assert values["date_from"] is not None and values["date_to"] is not None, \
                f"date_from, date_to is required for '{PrevSelected.prev_date}'"
        return values
