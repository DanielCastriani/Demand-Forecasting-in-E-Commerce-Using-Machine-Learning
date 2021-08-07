

from typing import List

import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy
from typehint.config_types import FeatureConfigs, LagConfig
from utils.date_utils import create_aggregation_cols, join_date


def aggregate(dataset: pd.DataFrame, date_cols: List[str], keys: List[str], values: List[str], targer: str):
    # Weighted Mean
    total = dataset.groupby([*keys, *date_cols]).sum()

    total.loc[:, values] = total.loc[:, values].div(total.loc[:, targer], axis=0)

    return total.reset_index()


def lag_feature(dataset: pd.DataFrame, grouped: DataFrameGroupBy, config: LagConfig):
    dataset = dataset.copy()
    arr_range = config.get('range')

    if not arr_range:
        if config['end']:
            arr_range = range(config['start'] or 1, int(config['end']) + 1, config['steps'] or 1)
        else:
            raise Exception("Missing 'end' or 'range' property")

    col = config["column"]

    lag_cols = []

    for w in arr_range:
        new_col = f'{col}_{-1*w}'

        dataset[new_col] = grouped[col].shift(w)
        dataset[new_col] = dataset[new_col].fillna(-1)

        lag_cols.append(new_col)

    return dataset, lag_cols


def lag_features(dataset: pd.DataFrame, lag_config_list: List[LagConfig], keys: List[str]):
    grouped = dataset.groupby(keys)
    lag_cols_list = []

    for c in lag_config_list:
        dataset, lag_cols = lag_feature(dataset, grouped, c)

        lag_cols_list = [*lag_cols_list, c['column'], *lag_cols]

    return dataset, lag_cols_list


def make_features(dataset: pd.DataFrame, config: FeatureConfigs, inplace: bool = False):
    if not inplace:
        dataset = dataset.copy()

    dataset = dataset[[config['date_column'], *config['keys'], *config['values'], config['target']]]

    dataset, date_cols = create_aggregation_cols(dataset, agg_mode=config['agg_mode'], date_col=config['date_column'])
    dataset = aggregate(dataset, date_cols, keys=config['keys'], values=config['values'], targer=config['target'])

    dataset = join_date(dataset, agg_mode=config['agg_mode'], column_name=config['date_column'])

    dataset['total'] = dataset['price'] + dataset['freight_value']

    dataset = dataset.sort_values('date')

    dataset, numeric_columns = lag_features(dataset, lag_config_list=config['lag_config'], keys=config['keys'])

    return dataset, numeric_columns
