

import logging
from itertools import product
from time import time
from typing import Any, Callable, Dict, List

import numpy as np
import pandas as pd
from tensorflow.keras import backend as K
from typehint.config_types import FeatureConfigs
from typehint.model_types import KerasCreateModelCallback

from utils.error_report import error_report
from utils.file_utils import create_path_if_not_exists, save_model_config
from utils.loggin_utils import calculate_elapsed_time, get_loggin


def create_model_folder(config: FeatureConfigs, regressor_name: str):
    model_name = f'{regressor_name}_{config["name"]}'
    model_path = create_path_if_not_exists('bin', model_name)

    save_model_config(config, model_path)
    return model_name, model_path


def grid_search_hist(error_list: List[dict]):
    error_df = pd.DataFrame(error_list)
    error_df = error_df.sort_values('mape')

    best = error_df.head(1).to_dict('records')[0]['config']
    return error_df, best


def grid_search_report(
        y_test: pd.Series, console: logging, total_iter: int, error_list: List[dict],
        i: int, config: Dict, start: float, predict: np.ndarray):
    error = error_report(y_test, predict)
    error_list.append({**error, 'config': config})

    error = {e: f'{error[e]:.3f}' for e in error if error.get(e)}

    console.info(f'{i + 1} / {total_iter} - {calculate_elapsed_time(start)} - {error}')


def generate_combination(grid_parameters: Dict[str, List[Any]]):
    console = get_loggin()

    combinations = product(*grid_parameters.values())

    configs = [dict(zip(grid_parameters, v)) for v in combinations]

    total_iter = len(configs)

    console.info(f'Grid search with {total_iter} combinations')

    error_list = []
    return console, configs, total_iter, error_list


def grid_search(
        Regressor: Any,
        grid_parameters: Dict[str, List[Any]],
        x_train: pd.DataFrame,
        y_train: pd.Series,
        x_test: pd.DataFrame,
        y_test: pd.Series):

    console, configs, total_iter, error_list = generate_combination(grid_parameters)

    for i, config in enumerate(configs):
        start = time()
        model = Regressor(**config)
        model.fit(x_train, y_train)
        predict = model.predict(x_test)

        grid_search_report(y_test, console, total_iter, error_list, i, config, start, predict)

    error_df, best = grid_search_hist(error_list)

    return best, error_df


def grid_search_keras(
        create_model_callback: KerasCreateModelCallback,
        grid_parameters: Dict[str, List[Any]],
        x_train: pd.DataFrame,
        y_train: pd.Series,
        x_test: pd.DataFrame,
        y_test: pd.Series):

    console, configs, total_iter, error_list = generate_combination(grid_parameters)

    input_size = len(x_train.columns)

    for i, config in enumerate(configs):
        start = time()

        model = create_model_callback(input_size, config=config['model'], lr=config['lr'])

        model.fit(x_train, y_train, batch_size=config['batch_size'], epochs=config['epochs'], verbose=False)
        predict = model.predict(x_test)

        grid_search_report(y_test, console, total_iter, error_list, i, config, start, predict)

        del model
        K.clear_session()

    error_df, best = grid_search_hist(error_list)

    return best, error_df
