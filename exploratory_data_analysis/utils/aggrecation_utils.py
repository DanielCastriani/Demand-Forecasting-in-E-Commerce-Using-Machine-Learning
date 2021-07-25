
from typing import List
from typehint import AggregationMode

import pandas as pd


def create_aggregation_cols(df: pd.DataFrame, agg_mode: AggregationMode, date_col: str = 'date'):

    cols = ['y']
    df['y'] = df[date_col].dt.year

    if agg_mode != 'y':
        cols.append('m')
        df['m'] = df[date_col].dt.month

        if agg_mode != 'm':
            cols.append('w')
            df['w'] = df[date_col].dt.isocalendar().week

            if agg_mode != 'w':
                cols.append('d')
                df['d'] = df[date_col].dt.day

    return df, cols


def aggregate(df: pd.DataFrame, agg_mode: AggregationMode, keys: List[str], agg_func: str = 'mean', date_col: str = 'date'):
    df, cols = create_aggregation_cols(df, agg_mode=agg_mode, date_col=date_col)

    return df.groupby(cols + keys).agg(agg_func).reset_index()
