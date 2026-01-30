from datetime import date, time
from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator

from .enums.interval import Selected, PrevSelected


class DateRange(BaseModel):
    selected: Selected = Selected.last_update_date
    date_from: Optional[date]
    date_to: Optional[date]

    model_config = ConfigDict(use_enum_values=True)

    @model_validator(mode="after")
    def date_range_require(self):
        if self.selected == Selected.date:
            assert (
                self.date_from is not None and self.date_to is not None
            ), f"date_from, date_to is required for '{Selected.date}'"
        return self

    @classmethod
    def default(cls):
        return cls()


class PrevDateRange(DateRange):
    selected: PrevSelected = PrevSelected.previous

    @model_validator(mode="after")
    def prev_date_range_require(self):
        if self.selected == PrevSelected.prev_date:
            assert (
                self.date_from is not None and self.date_to is not None
            ), f"date_from, date_to is required for '{PrevSelected.prev_date}'"
        return self


class TimeRange(BaseModel):
    time_from: time = time(0, 0, 0)
    time_to: time = time(23, 59, 59)

    @classmethod
    def default(cls):
        return cls()
