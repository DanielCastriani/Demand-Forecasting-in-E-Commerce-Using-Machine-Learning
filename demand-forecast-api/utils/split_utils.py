import pandas as pd


def split_train_test(dataset: pd.DataFrame, test_date: str, date_column: str = 'date', verbose: bool = False):
    train = dataset[dataset[date_column] < test_date]
    test = dataset[dataset[date_column] >= test_date]

    return train, test
