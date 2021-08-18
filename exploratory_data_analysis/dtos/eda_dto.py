

from typing import TypedDict

import pandas as pd


class FeatureSummaryDTO(TypedDict):
    rows: int
    nunique: int
    df: pd.DataFrame


class DatasetInfoSummary(TypedDict):
    mean_product_qty: float
    total_qty: float

    mean_days_to_approve: float

    mean_days_to_post: float
    min_days_to_post: float
    max_days_to_post: float

    mean_days_to_deliver: float
    min_days_to_deliver: float
    max_days_to_deliver: float

    mean_days_estimated_to_deliver: float
    min_days_estimated_to_deliver: float
    max_days_estimated_to_deliver: float

    mean_product_profit: float
    total_profit: float
