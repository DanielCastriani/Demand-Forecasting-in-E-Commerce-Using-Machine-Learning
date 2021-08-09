from typing import Union

import pandas as pd


def filter_df(df: pd.DataFrame, column: str, value: Union[str, int] = -1):
    if column in df.columns and value is not None and value != -1:
        df = df[df[column] == value]

    return df