from enum import Enum


class Condition(str, Enum):
    eq = "eq"
    ne = "ne"
    gt = "gt"
    ge = "ge"
    lt = "lt"
    le = "le"
    top = "top"
    bottom = "bottom"


class DType(str, Enum):
    string = "string"
    number = "number"
    boolean = "boolean"
    array = "array"
    object = "object"
    date = "date"
    time = "time"
    datetime = "datetime"
