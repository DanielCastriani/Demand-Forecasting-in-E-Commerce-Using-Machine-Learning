
from typing import Any

import pandas as pd

from utils.error_report import error_report
from utils.file_utils import create_path_if_not_exists


def save_report(
        model_path: str,
        train_keys: pd.DataFrame,
        test_keys: pd.DataFrame,
        x_train: pd.DataFrame,
        y_train: pd.Series,
        x_test: pd.DataFrame,
        y_test: pd.Series,
        model: Any):

    predict_train = model.predict(x_train)
    predict_test = model.predict(x_test)

    train_error = error_report(y_train, predict_train)
    test_error = error_report(y_test, predict_test)

    error_df = pd.DataFrame([train_error, test_error], index=['train', 'test'])
    print(error_df)

    error_df.to_csv(create_path_if_not_exists(model_path, filename=f'erro.csv'))

    train_keys['type'] = 'train'
    test_keys['type'] = 'test'

    train_keys['real'] = y_train
    test_keys['real'] = y_test

    train_keys['predicted'] = predict_train
    test_keys['predicted'] = predict_test

    result = pd.concat([train_keys, test_keys])
    result.to_csv(create_path_if_not_exists(model_path, filename=f'results.csv'))
