from typing import List
import pandas as pd


def lag_feature(
        df: pd.DataFrame,
        keys: List[str],
        column: str,
        window: int = None,
        start: int = 1,
        steps: int = 1,
        range_list: List[int] = None):
    
    df = df.copy()

    if not range_list:
        if not window:
            raise ValueError('neither window, nor range_list was defined')
        else:
            range_list = range(start, window + 1, steps)

    grouped_df = df.groupby(keys)

    for i in range_list:
        df[f'{column}_{-i}'] = grouped_df[column].shift(i)

    return df


def lag_columns(df: pd.DataFrame, lag_feature_column: str, ext: List[str] = []):
    return [c for c in df.columns if c.startswith(lag_feature_column)] + ext
