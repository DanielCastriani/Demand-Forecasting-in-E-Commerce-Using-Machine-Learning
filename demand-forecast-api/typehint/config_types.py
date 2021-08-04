

from typing import List, Optional, TypedDict
from typehint.base_types import AggregationMode


class ConfigType(TypedDict):
    hdfs: str
    N_JOBS: int


class LagConfig(TypedDict):
    start: Optional[int]
    end: Optional[int]
    steps: Optional[int]

    range: Optional[List[int]]
    column: str


class FeatureConfigs(TypedDict):
    name: str
    agg_mode: AggregationMode
    date_column: str
    keys: List[str]
    lag_config: List[LagConfig]
    target: str
    values: List[str]
