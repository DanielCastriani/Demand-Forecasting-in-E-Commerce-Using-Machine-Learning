from configs.feature_config import DATE_COLUMN
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
        train = train.drop(columns=[DATE_COLUMN])
        test = test.drop(columns=[DATE_COLUMN])

    if verbose:
        total = len(dataset)
        print(f'Train: {len(train)/total * 100:.3f}%')
        print(f'Test: {len(test)/total * 100:.3f}%')

    return train.reset_index(drop=True), test.reset_index(drop=True)


def split_x_y(dataset: pd.DataFrame, target: str):
    y = dataset[target]
    x = dataset.drop(columns=[target])

    return x[sorted(x.columns)], y
