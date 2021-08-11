from typing import List
from typehint.config_types import FeatureConfigs
from utils.preprocessing.apply_preprocessing import apply_preprocessing
import pandas as pd


def split_train_test_timeseries(
        dataset: pd.DataFrame,
        test_date: str,
        date_column: str = 'date',
        verbose: bool = False,
        drop_date_columns: bool = True):

    train = dataset[dataset[date_column] < test_date]
    test = dataset[dataset[date_column] >= test_date]

    if drop_date_columns:
        train = train.drop(columns=[date_column])
        test = test.drop(columns=[date_column])

    if verbose:
        total = len(dataset)
        len_train = len(train)
        len_test = len(test)
        print(f'Train: {len_train/total * 100:.3f}%\t\t{len_train}')
        print(f'Test: {len_test/total * 100:.3f}%\t\t{len_test}')

    return train.reset_index(drop=True), test.reset_index(drop=True)


def split_x_y(dataset: pd.DataFrame, target: str):
    y = dataset[target]
    x = dataset.drop(columns=[target])

    return x[sorted(x.columns)], y


def split_pipeline(test_date: str, config: FeatureConfigs, model_path: str, dataset: pd.DataFrame, numeric_columns: List[str]):
    train, test = split_train_test_timeseries(dataset, test_date=test_date, verbose=True, drop_date_columns=False)

    train, _, _, train_keys = apply_preprocessing(
        train,
        config=config,
        numeric_columns=numeric_columns,
        model_path=model_path,
        train=True,
    )

    test, _, _, test_keys = apply_preprocessing(
        test,
        config=config,
        numeric_columns=numeric_columns,
        model_path=model_path,
        train=False,
    )

    x_train, y_train = split_x_y(train, config['target'])
    x_test, y_test = split_x_y(test, config['target'])
    return train_keys, test_keys, x_train, y_train, x_test, y_test
