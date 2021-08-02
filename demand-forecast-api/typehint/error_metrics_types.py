from typing import TypedDict


class ErrorMetrics(TypedDict):
    mse: float
    mae: float
    mape: float
    r2: float
    corr: float
