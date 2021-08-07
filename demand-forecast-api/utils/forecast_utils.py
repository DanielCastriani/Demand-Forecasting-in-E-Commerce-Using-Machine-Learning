

import pandas as pd
from feature_engineering.make_features import make_features
from typehint.config_types import FeatureConfigs


def prepare_data_forecast(config: FeatureConfigs, dataset: pd.DataFrame):
    max_lag = max([int(x.get('end')) +1 if x.get('end') else max(x['range']) for x in config['lag_config']])

    filter_date = dataset['date'].max() - pd.Timedelta(days=max_lag)
    dataset = dataset[dataset['date'] >= filter_date]

    df, numeric_cols = make_features(dataset, config)

    df = df.groupby(config['keys']).tail(1)
    df['date'] = dataset['date'].max() + pd.Timedelta(days=1)

    return df, numeric_cols