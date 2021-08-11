

import pandas as pd
from feature_engineering.make_features import make_features
from typehint.config_types import FeatureConfigs


def prepare_data_forecast(config: FeatureConfigs, forecast_dataset: pd.DataFrame):

    filter_date = forecast_dataset['date'] >= forecast_dataset['date'].max() - pd.Timedelta(days=395)
    forecast_dataset = forecast_dataset[filter_date]

    forecast_dataset, numeric_cols = make_features(forecast_dataset, config)
    forecast_dataset = forecast_dataset.reset_index(drop=True)

    forecast_data = forecast_dataset.groupby(config['keys']).tail(1).copy(deep=True)

    max_date = forecast_data['date'].max()
    if config['agg_mode'] == 'm':
        forecast_data['date'] = max_date + pd.Timedelta(days=32)
        forecast_data['date'] = forecast_data['date'].apply(lambda dt: pd.to_datetime(f'{dt.year}-{dt.month}-1'))
    elif config['agg_mode'] == 'w':
        forecast_data['date'] = max_date + pd.Timedelta(days=15)
    else:
        forecast_data['date'] = max_date + pd.Timedelta(days=1)

    return forecast_data, forecast_dataset, numeric_cols
