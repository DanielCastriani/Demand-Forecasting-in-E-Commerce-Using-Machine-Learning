import os
import pickle
from typing import List

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from utils.file_utils import create_path_if_not_exists


def normalizer(
        dataset: pd.DataFrame,
        columns: List[str],
        path: str = 'bin',
        file_name: str = 'scaler.pickle',
        train: bool = True):

    values = dataset[columns].values

    if train:

        scaler = MinMaxScaler()

        scaler.fit(values)

        with open(create_path_if_not_exists(path, filename=file_name), 'wb') as f:
            pickle.dump({
                'scaler': scaler,
                'columns': columns
            }, f)

    else:
        scaler, columns = load_one_hot_encoder(path=path, file_name=file_name)

    values = scaler.transform(values)

    dataset[columns] = values

    return dataset, columns


def load_one_hot_encoder(path: str = 'bin', file_name: str = 'one_hot_encoder.pickle'):
    path = os.path.join(path, file_name)

    with open(path, 'rb') as f:
        enc_dict = pickle.load(f)

    return enc_dict['scaler'], enc_dict['columns']
