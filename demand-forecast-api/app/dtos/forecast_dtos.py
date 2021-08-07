
from typing import TypedDict


class ForecastRequestDTO(TypedDict):
    model_name: str
    window_size: int