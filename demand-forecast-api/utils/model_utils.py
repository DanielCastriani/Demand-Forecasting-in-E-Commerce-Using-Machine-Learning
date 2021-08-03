

from time import time
from typing import Any, Dict, List
from utils.error_report import error_report
from utils.loggin_utils import calculate_elapsed_time, get_loggin
from typehint.config_types import FeatureConfigs
from utils.file_utils import create_path_if_not_exists, save_model_config
import pandas as pd

from itertools import product


def create_model_folder(config: FeatureConfigs, regressor_name: str):
    model_name = f'{regressor_name}_{config["name"]}'
    model_path = create_path_if_not_exists('bin', model_name)

    save_model_config(config, model_path)
    return model_name, model_path


def grid_search(
        Regressor: Any,
        grid_parameters: Dict[str, List[Any]],
        x_train: pd.DataFrame,
        y_train: pd.Series,
        x_test: pd.DataFrame,
        y_test: pd.Series):
    console = get_loggin()

    combinations = product(*grid_parameters.values())

    configs = [dict(zip(grid_parameters, v)) for v in combinations]

    total_iter = len(configs)

    console.info(f'Grid search with {total_iter} combinations')

    error_list = []

    for i, config in enumerate(configs):
        start = time()
        model = Regressor(**config)
        model.fit(x_train, y_train)
        predict = model.predict(x_test)

        error = error_report(y_test, predict)
        error_list.append({**error, 'config': config})

        console.info(f'{i + 1} / {total_iter} - {calculate_elapsed_time(start)} - {error}')

    error_df = pd.DataFrame(error_list)
    error_df = error_df.sort_values('mape')

    best = error_df.head(1).to_dict('records')[0]['config']

    return best, error_df
