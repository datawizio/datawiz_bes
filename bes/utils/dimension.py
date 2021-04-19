from typing import List

LOOKUP_SEP = "__"


def dimension_display_fields(dimension: str, display_fields) -> List[str]:
    return [f"{dimension}{LOOKUP_SEP}{display_field}" for display_field in display_fields]
