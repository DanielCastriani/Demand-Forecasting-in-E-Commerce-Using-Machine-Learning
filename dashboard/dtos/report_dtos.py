from typing import Any, Dict, List, TypedDict


class ReportItem(TypedDict):
    name: str
    keys: List[str]
    agg_mode: str


class ReportDTO(TypedDict):
    filters: Dict[str, List[Any]]
    data: Dict


