

from utils.split_utils import split_pipeline
from feature_engineering.make_features import make_features
import json
from utils.dataset_utils import load_dataset

from configs.feature_config import config_list
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from utils.config_utils import get_configs
from utils.loggin_utils import get_loggin, timer
from utils.model_utils import create_model_folder


def train_tree():
    test_date = '2018-05-01'

    console = get_loggin()
    console.info(json.dumps(get_configs(), indent=4))

    regressor_list = [RandomForestRegressor, GradientBoostingRegressor]

    for Regressor in regressor_list:

        for config in config_list:
            model_name, model_path = create_model_folder(config)

            with timer(loggin_name='train', message_prefix=f'train {model_name}'):
                dataset = load_dataset()
                dataset, numeric_columns = make_features(dataset, config=config)

                train_keys, test_keys, x_train, y_train, x_test, y_test = split_pipeline(
                    test_date,
                    config,
                    model_path,
                    dataset,
                    numeric_columns)
