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

            index_list = [tuple(v) for v in forecast_data[[*keys, 'date']].values]
            forecast_result = [*forecast_result, *index_list]

            forecast_dataset = pd.concat([forecast_dataset, forecast_data.copy(deep=True)])
            forecast_dataset = forecast_dataset.reset_index(drop=True)

        forecast_dataset = forecast_dataset.set_index([*keys, 'date'])
        forecast_dataset.loc[forecast_dataset.index.isin(forecast_result), 'type'] = 'forecast'
        forecast_dataset['type'] = forecast_dataset['type'].fillna('real')
        forecast_dataset = forecast_dataset.reset_index()

        forecast_dataset = forecast_dataset[['date', 'type', *config['keys'], config['target']]]

        for i in range(1, body['window_size']+1):
            forecast_dataset[f"{config['target']}_{i*-1}"] = forecast_dataset.groupby(config['keys'])[config['target']].shift(i)

        forecast_dataset = forecast_dataset.fillna(0)

        return forecast_dataset, config['agg_mode']
