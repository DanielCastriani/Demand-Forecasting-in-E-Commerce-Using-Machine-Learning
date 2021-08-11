
from typing import Dict, Optional, TypedDict, Union


class ReportFilter(TypedDict):
    is_delayed: Optional[Union[str, bool]]
    order_status: Optional[str]
    product_category_name: Optional[str]
    seller_id: Optional[str]
    datatype: Optional[str]


class ForecastRequestDTO(ReportFilter):
    model_name: str
    window_size: int
    aggregate_results: bool


class ForecastResponseDTO(TypedDict):
    result: Dict
    filter: Dict
