import os

import pandas as pd
from scipy.sparse import data
from app.dtos.forecast_dtos import ForecastRequestDTO
from typehint.config_types import FeatureConfigs
from utils.file_utils import load_model
from utils.forecast_utils import prepare_data_forecast
from utils.preprocessing.apply_preprocessing import apply_preprocessing
from utils.split_utils import split_x_y


def forecast(config: FeatureConfigs, dataset: pd.DataFrame, body: ForecastRequestDTO):
    window = body['window_size']
    model_name = body['model_name']

    root_path = os.path.join('bin', model_name)
    model = load_model(os.path.join(root_path, 'model.pickle'))

    df_original = dataset.copy()

    df_original = df_original[(df_original['product_category_name'] == 'utilidades_domesticas')
                              & (df_original['order_status'] == 'delivered')]

    if model:

        results = []

        for _ in range(window):
            forecast_data, df_original, numeric_cols = prepare_data_forecast(config, df_original)

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

            results.append(forecast_data)
            df_original = pd.concat([df_original, forecast_data])

        result = pd.concat(results)

        qty_cols = [config['target'], *[f"{config['target']}_{i*-1}" for i in range(1, body['window_size']+1)]]

        result = result[['date', *config['keys'], *qty_cols]].reset_index(drop=True)

        for i in range(1, body['window_size']+1):
            result[f"{config['target']}_{i*-1}"] = result.groupby(config['keys'])[config['target']].shift(i)

        return result
