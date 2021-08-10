

import pandas as pd
from feature_engineering.make_features import make_features
from typehint.config_types import FeatureConfigs


def prepare_data_forecast(config: FeatureConfigs, dataset: pd.DataFrame):
    max_lag = max([int(x.get('end')) + 1 if x.get('end') else max(x['range']) for x in config['lag_config']])

    if config['agg_mode'] == 'm':
        max_lag *= 31
    elif config['agg_mode'] == 'w':
        max_lag *= 7

    filter_date = dataset['date'].max() - pd.Timedelta(days=max_lag)
    dataset = dataset[dataset['date'] >= filter_date]

    df, numeric_cols = make_features(dataset, config)
    df = df.reset_index(drop=True)

    df_original = df[[c for c in df.columns if '_-' not in c]].copy()

    df = df.groupby(config['keys']).tail(1).copy()

    if config['agg_mode'] == 'm':
        df['date'] = df['date'].max() + pd.Timedelta(days=31)
    elif config['agg_mode'] == 'w':
        df['date'] = df['date'].max() + pd.Timedelta(weeks=1)
    else:
        df['date'] = df['date'].max() + pd.Timedelta(days=1)

    return df, df_original, numeric_cols
