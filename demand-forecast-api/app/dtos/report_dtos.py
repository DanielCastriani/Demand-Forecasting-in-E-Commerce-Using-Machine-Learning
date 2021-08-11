from typehint.base_types import AggregationMode
from typing import Any, Dict, List, Optional, TypedDict, Union


class ReportItem(TypedDict):
    name: str
    keys: List[str]
    agg_mode: AggregationMode


class ReportDTO(TypedDict):
    filters: Dict[str, List[Any]]
    data: Dict


class ReportFilter(TypedDict):
    is_delayed: Optional[Union[str, bool]]
    order_status: Optional[str]
    product_category_name: Optional[str]
    seller_id: Optional[str]


class RequestReportDTO(ReportFilter):
    model_name: str
    datatype: Optional[str]
