from enum import Enum


class By(str, Enum):
    id = "id"
    parent_id = "parent_id"
    level = "level"


class Mode(str, Enum):
    and_ = "and"
    or_ = "or"


class On(str, Enum):
    column = "column"
    row = "row"
