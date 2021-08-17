
from typing import Dict, TypedDict
from app.dtos.report_dtos import ReportFilter


class ForecastRequestDTO(ReportFilter):
    model_name: str
    window_size: int


class ForecastResponseDTO(TypedDict):
    result: Dict
    filter: Dict
    agg_mode: str
