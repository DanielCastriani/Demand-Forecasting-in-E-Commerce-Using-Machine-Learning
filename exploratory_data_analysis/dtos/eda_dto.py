

from typing import TypedDict

import pandas as pd


class CustomerSummaryDTO(TypedDict):
    rows: int
    nunique: int
    costumers: pd.DataFrame
