

from typing import List, Optional, TypedDict


class ConfigType(TypedDict):
    hdfs: str
    n_jobs: int


class LagConfig(TypedDict):
    start: Optional[int]
    end: Optional[int]
    steps: Optional[int]

    range: Optional[List[int]]
    column: str
