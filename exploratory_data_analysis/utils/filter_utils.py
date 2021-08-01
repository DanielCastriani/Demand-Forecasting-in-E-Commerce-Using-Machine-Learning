from typing import Union

import pandas as pd


def filter_df(df: pd.DataFrame, column: str, value: Union[str, int] = -1):
    if value != -1:
        df = df[df[column] == value]

    return df
