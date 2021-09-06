from typing import Optional

from pydantic import BaseModel

from .enums.options import RenderType, DataFrameFormatType, DeltaInterval


class Options(BaseModel):
    with_col_total: bool = False
    with_row_total: bool = False
    use_cache: bool = False
    delta_interval: DeltaInterval = DeltaInterval.day_month_year
    reindex_data: bool = True
    concat_dimensions: bool = False
    fixed_total: bool = False

    class Config:
        use_enum_values = True

    @classmethod
    def default(cls):
        return cls()


class RenderOptions(BaseModel):
    dtype: RenderType

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True

    @classmethod
    def default(cls):
        return cls(
            dtype=RenderType.table
        )


class TableRenderOptions(RenderOptions):
    dtype: RenderType = RenderType.table
    additional_data: Optional[dict]
    additional_column_options: Optional[dict]
    replace_data: Optional[dict]
    clone_data: Optional[dict]
    key_start: Optional[str]


class ChartRenderOptions(RenderOptions):
    dtype: RenderType = RenderType.chart
    additional_data: Optional[dict]
    replace_data: Optional[dict]
    clone_data: Optional[dict]
    key_start: Optional[str]


class DataFrameRenderOptions(RenderOptions):
    dtype: RenderType = RenderType.data_frame
    format_type: DataFrameFormatType = DataFrameFormatType.split
