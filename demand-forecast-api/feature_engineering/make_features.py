

from typing import List

import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy
from typehint.config_types import LagConfig
from utils.date_utils import create_aggregation_cols, join_date

KEYS = [
    'seller_state',
    'product_category_name',
    'product_id',
    'order_status',
    'is_delayed',
]

VALUES = [
    'days_to_approve',
    'days_to_post',
    'days_to_deliver',
    'days_estimated_to_deliver',
    'estimated_delivered_diff',
    'price',
    'freight_value',
    'total',
    'product_name_lenght',
    'product_description_lenght',
    'product_photos_qty',
    'product_weight_g',
    'product_length_cm',
    'product_height_cm',
    'product_width_cm',
    'dollar',
    'ipca'
]

DATE_COLUMN = 'date'
TARGET = 'qty'

AGG_MODE = 'w'

LAG_CONFIG = [
    LagConfig(start=1, end=54, steps=1, column=TARGET),
    LagConfig(start=1, end=16, steps=1, column='days_to_approve'),
    LagConfig(start=1, end=24, steps=1, column='days_to_post'),
    LagConfig(start=1, end=24, steps=1, column='days_to_deliver'),
    LagConfig(start=1, end=24, steps=1, column='days_estimated_to_deliver'),
    LagConfig(start=1, end=24, steps=1, column='estimated_delivered_diff'),
    LagConfig(start=1, end=54, steps=1, column='price'),
    LagConfig(start=1, end=54, steps=1, column='freight_value'),
    LagConfig(start=1, end=54, steps=1, column='total'),
    LagConfig(start=1, end=24, steps=1, column='product_name_lenght'),
    LagConfig(start=1, end=24, steps=1, column='product_description_lenght'),
    LagConfig(start=1, end=24, steps=1, column='product_photos_qty'),
    LagConfig(start=1, end=24, steps=1, column='product_weight_g'),
    LagConfig(start=1, end=24, steps=1, column='product_length_cm'),
    LagConfig(start=1, end=24, steps=1, column='product_height_cm'),
    LagConfig(start=1, end=24, steps=1, column='product_width_cm'),
    LagConfig(start=1, end=54, steps=1, column='dollar'),
    LagConfig(start=1, end=54, steps=1, column='ipca'),
]


def aggregate(dataset: pd.DataFrame, date_cols: List[str]):
    # Weighted Mean
    total = dataset.groupby([*KEYS, *date_cols]).sum()

    total.loc[:, VALUES] = total.loc[:, VALUES].div(total.loc[:, TARGET], axis=0)

    return total.reset_index()


def lag_feature(dataset: pd.DataFrame, grouped: DataFrameGroupBy, config: LagConfig):
    dataset = dataset.copy()
    arr_range = config.get('range')

    if not arr_range:
        arr_range = range(config['start'], config['end'], config['steps'] + 1)

    col = config["column"]

    for w in arr_range:
        new_col = f'{col}_{-1*w}'
        dataset[new_col] = grouped[col].shift(w)
        dataset[new_col] = dataset[new_col].fillna(-1)

    return dataset


def lag_features(dataset: pd.DataFrame):
    grouped = dataset.groupby(KEYS)
    for c in LAG_CONFIG:
        dataset = lag_feature(dataset, grouped, c)

    return dataset


def make_features(dataset: pd.DataFrame, inplace: bool = False):
    if not inplace:
        dataset = dataset.copy()

    dataset = dataset[[DATE_COLUMN, *KEYS, *VALUES, TARGET]]

    dataset, date_cols = create_aggregation_cols(dataset, agg_mode=AGG_MODE, date_col=DATE_COLUMN)
    dataset = aggregate(dataset, date_cols)

    dataset = join_date(dataset, agg_mode=AGG_MODE, column_name=DATE_COLUMN)

    dataset['total'] = dataset['price'] + dataset['freight_value']

    dataset = lag_features(dataset)

    return dataset
