from typing import Literal
from typehint.config_types import *

FileMode = Literal['r', 'w', 'a']
AggregationMode = Literal['y', 'm', 'w', 'd']


class ErrorMetrics(TypedDict):
    mse: float
    mae: float
    mape: float
    r2: float
    corr: float
