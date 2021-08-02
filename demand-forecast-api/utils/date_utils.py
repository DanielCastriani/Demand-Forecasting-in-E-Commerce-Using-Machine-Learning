
from datetime import datetime
from typehint import AggregationMode
import pandas as pd


def create_aggregation_cols(df: pd.DataFrame, agg_mode: AggregationMode, date_col: str = 'date', inplace: bool = False):

    if not inplace:
        df = df.copy()

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


def join_date(df: pd.DataFrame, agg_mode: AggregationMode, column_name='date', inplace: bool = False):

    if not inplace:
        df = df.copy()

    def strptime(s: pd.Series, agg_mode: AggregationMode):

        if agg_mode == 'y':
            return datetime(year=int(s['y']), month=1, day=1)
        elif agg_mode == 'm':
            return datetime(year=int(s['y']), month=int(s['m']), day=1)
        elif agg_mode == 'w':
            return datetime.strptime(f"{int(s['y'])}-{int(s['w']) - 1}-0", '%Y-%W-%w')
        else:
            return datetime(year=s['y'], month=s['m'], day=s['d'])

    df[column_name] = df.apply(lambda s: strptime(s, agg_mode), axis=1)

    cols = ['y']
    if agg_mode != 'y':
        cols.append('m')
        if agg_mode != 'm':
            cols.append('w')
            if agg_mode != 'w':
                cols.append('d')

    df = df.drop(columns=cols)
    return df
