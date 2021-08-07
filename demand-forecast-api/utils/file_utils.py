import json
import os
import pickle
from typing import Any

from tensorflow import keras
from typehint.config_types import FeatureConfigs


def create_path_if_not_exists(*args, filename: str = None) -> str:
    path = os.path.join(*args)
    if not os.path.exists(path):
        os.makedirs(path)

    if filename:
        return os.path.join(path, filename)

    return path


def save_model(model: Any, model_path: str = 'bin/', file_name: str = 'model.pickle'):
    with open(create_path_if_not_exists(model_path, filename=file_name), 'wb') as f:
        pickle.dump(model, f)


def load_model(model_path: str = 'bin/model.pickle'):
    try:
        with open(model_path, 'rb') as f:
            return pickle.load(f)

    except:
        model_path = model_path.replace('.pickle', '')
        return keras.models.load_model(model_path)

def save_model_config(config: FeatureConfigs, model_path: str, file_name: str = 'config.json'):
    with open(create_path_if_not_exists(model_path, filename=file_name), 'w') as f:
        json.dump(config, f, indent=4)
