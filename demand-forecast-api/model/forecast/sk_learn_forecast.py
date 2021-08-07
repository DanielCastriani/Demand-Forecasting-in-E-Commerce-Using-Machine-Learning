import os

import pandas as pd
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
    model = load_model(os.path.join( root_path, 'model.pickle'))

    if model:

        results  = []

        for _ in range(window):

            forecast_dataset, numeric_cols = prepare_data_forecast(config, dataset)
            forecast_dataset = forecast_dataset.reset_index(drop=True)

            forecast_df, _, _, _ = apply_preprocessing(
                df=forecast_dataset,
                config=config,
                numeric_columns=numeric_cols,
                model_path=root_path,
                train=False,
            )
            x, _ = split_x_y(forecast_df, config['target'])

            y = model.predict(x)

            forecast_dataset[config['target']] = y

            results.append(forecast_dataset)
            dataset = pd.concat([dataset, forecast_dataset])


        result = pd.concat(results)

        return result[['date', *config['keys'], config['target']]]
