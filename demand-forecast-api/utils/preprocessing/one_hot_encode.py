import os
import pickle
from typing import List

import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from utils.file_utils import create_path_if_not_exists


def one_hot_encoder(
        dataset: pd.DataFrame,
        keys: List[str],
        path: str = 'bin',
        file_name: str = 'one_hot_encoder.pickle',
        train: bool = True):
    keys = [c for c in keys if c != 'product_id']

    arr = dataset[keys].values

    if train:
        categories = [dataset[c].unique() for c in keys]
        enc = OneHotEncoder(
            handle_unknown='ignore',
            categories=categories,
        )

        enc.fit(arr)

        columns = []

        for c in keys:
            columns += [f'{c}_{value}' for value in dataset[c].unique().tolist()]

        with open(create_path_if_not_exists(path, filename=file_name), 'wb') as f:
            pickle.dump({
                'encoder': enc,
                'columns': columns
            }, f)

    else:
        enc, columns = load_one_hot_encoder(path=path, file_name=file_name)

    values = enc.transform(arr).toarray()

    cat = pd.DataFrame(values, columns=columns)

    df = pd.concat([dataset.reset_index(drop=True), cat], axis=1)

    keys_df = df[keys].copy()
    keys_df = keys_df.reset_index(drop=True)

    df = df.drop(columns=keys)

    return df, keys_df, columns


def load_one_hot_encoder(path: str = 'bin', file_name: str = 'one_hot_encoder.pickle'):
    path = os.path.join(path, file_name)

    with open(path, 'rb') as f:
        enc_dict = pickle.load(f)

    return enc_dict['encoder'], enc_dict['columns']
