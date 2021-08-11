from app.dtos.report_dtos import ReportFilter
from typing import Union

import pandas as pd


def filter_df(df: pd.DataFrame, column: str, value: Union[str, int] = -1):
    if column in df.columns and value is not None and value != -1:
        df = df[df[column] == value]

    return df


def apply_filter(body: ReportFilter, df: pd.DataFrame):
    body['is_delayed'] = bool(body.get('is_delayed')) if body.get('is_delayed') else None

    df = filter_df(df, column='is_delayed', value=body.get('is_delayed', -1))
    df = filter_df(df, column='order_status', value=body.get('order_status', -1))
    df = filter_df(df, column='product_category_name', value=body.get('product_category_name', -1))
    df = filter_df(df, column='seller_id', value=body.get('seller_id', -1))
    df = filter_df(df, column='type', value=body.get('datatype', -1))
    
    return df