

from typehint.config_types import FeatureConfigs
from utils.file_utils import create_path_if_not_exists, save_model_config


def create_model_folder(config: FeatureConfigs):
    model_name = f'knn_{config["name"]}'
    model_path = create_path_if_not_exists('bin', model_name)

    save_model_config(config, model_path)
    return model_name, model_path


    