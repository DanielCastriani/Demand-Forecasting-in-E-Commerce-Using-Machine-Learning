import os

import pandas as pd
from app.dtos.forecast_dtos import ForecastRequestDTO
from scipy.sparse import data
from typehint.config_types import FeatureConfigs
from utils.file_utils import load_model
from utils.forecast_utils import prepare_data_forecast
from utils.preprocessing.apply_preprocessing import apply_preprocessing
from utils.split_utils import split_x_y


def forecast(config: FeatureConfigs, dataset: pd.DataFrame, body: ForecastRequestDTO):
    window = body['window_size']
    model_name = body['model_name']
    keys = config['keys']

    root_path = os.path.join('bin', model_name)
    model = load_model(os.path.join(root_path, 'model.pickle'))

    forecast_dataset = dataset.copy()
    lim_dates = forecast_dataset.groupby(keys)['date'].max()

    if model:

        forecast_result = []

        while window > 0:
            window -= 1

            forecast_data, forecast_dataset, numeric_cols = prepare_data_forecast(config, forecast_dataset)

            forecast_df, _, _, _ = apply_preprocessing(
                df=forecast_data,
                config=config,
                numeric_columns=numeric_cols,
                model_path=root_path,
                train=False,
            )

            x, _ = split_x_y(forecast_df, config['target'])

            y = model.predict(x)

            forecast_data[config['target']] = y
            forecast_result.append(forecast_data)

            forecast_dataset = pd.concat([forecast_dataset, forecast_data.copy(deep=True)])
            forecast_dataset = forecast_dataset.reset_index(drop=True)

        def create_flag(df: pd.DataFrame):
            lim = lim_dates[df.name]
            df.loc[df['date'] >= lim, 'type'] = 'forecast'
            df.loc[df['date'] < lim, 'type'] = 'real'

            return df

        forecast_dataset = forecast_dataset.groupby(keys).apply(create_flag)

        forecast_dataset = forecast_dataset[['date', 'type', *config['keys'], config['target']]]

        for i in range(1, body['window_size']+1):
            forecast_dataset[f"{config['target']}_{i*-1}"] = forecast_dataset.groupby(config['keys'])[config['target']].shift(i)

        forecast_dataset = forecast_dataset.fillna(0)

        return forecast_dataset
