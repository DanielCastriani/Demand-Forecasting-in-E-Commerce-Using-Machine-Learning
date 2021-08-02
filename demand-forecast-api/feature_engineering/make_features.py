

from configs.feature_config import AGG_MODE, DATE_COLUMN, KEYS, LAG_CONFIG, TARGET, VALUES
from typing import List

import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy
from typehint.config_types import LagConfig
from utils.date_utils import create_aggregation_cols, join_date


def aggregate(dataset: pd.DataFrame, date_cols: List[str]):
    # Weighted Mean
    total = dataset.groupby([*KEYS, *date_cols]).sum()

    total.loc[:, VALUES] = total.loc[:, VALUES].div(total.loc[:, TARGET], axis=0)

    return total.reset_index()


def lag_feature(dataset: pd.DataFrame, grouped: DataFrameGroupBy, config: LagConfig):
    dataset = dataset.copy()
    arr_range = config.get('range')

    if not arr_range:
        arr_range = range(config['start'], config['end'] + 1, config['steps'])

    col = config["column"]

    lag_cols = []

    for w in arr_range:
        new_col = f'{col}_{-1*w}'

        dataset[new_col] = grouped[col].shift(w)
        dataset[new_col] = dataset[new_col].fillna(-1)

        lag_cols.append(new_col)

    return dataset, lag_cols


def lag_features(dataset: pd.DataFrame):
    grouped = dataset.groupby(KEYS)
    lag_cols_list = []

    for c in LAG_CONFIG:
        dataset, lag_cols = lag_feature(dataset, grouped, c)

        lag_cols_list = [*lag_cols_list, c['column'], *lag_cols]

    return dataset, lag_cols_list


def make_features(dataset: pd.DataFrame, inplace: bool = False):
    if not inplace:
        dataset = dataset.copy()

    dataset = dataset[[DATE_COLUMN, *KEYS, *VALUES, TARGET]]

    dataset, date_cols = create_aggregation_cols(dataset, agg_mode=AGG_MODE, date_col=DATE_COLUMN)
    dataset = aggregate(dataset, date_cols)

    dataset = join_date(dataset, agg_mode=AGG_MODE, column_name=DATE_COLUMN)

    dataset['total'] = dataset['price'] + dataset['freight_value']

    dataset, numeric_columns = lag_features(dataset)

    return dataset, numeric_columns
