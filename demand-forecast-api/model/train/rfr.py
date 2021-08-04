

import json

from configs.feature_config import config_list
from feature_engineering.make_features import make_features
from sklearn.ensemble import RandomForestRegressor
from utils.config_utils import get_config
from utils.dataset_utils import load_dataset
from utils.file_utils import create_path_if_not_exists, save_model
from utils.loggin_utils import get_loggin, timer
from utils.model_utils import create_model_folder, grid_search
from utils.report_utils import save_report
from utils.split_utils import split_pipeline


def train_tree():
    test_date = '2018-05-01'

    console = get_loggin()
    console.info(f'N_JOBS: {get_config("N_JOBS")}')

    grid_parameters = {
        'N_JOBS': [get_config('N_JOBS')],
        'n_estimators': [75, 150, 200],
        'max_depth': [100, None],
        'min_samples_split': [2, 4],
        'min_samples_leaf': [1, 2]
    }

    with timer(loggin_name='train', message_prefix=f'Train Tree algorithms'):
        for config in config_list:
            model_name, model_path = create_model_folder(config, regressor_name='RandomForestRegressor')

            with timer(loggin_name='train', message_prefix=f'train {model_name}'):
                dataset = load_dataset()
                dataset, numeric_columns = make_features(dataset, config=config)

                train_keys, test_keys, x_train, y_train, x_test, y_test = split_pipeline(
                    test_date,
                    config,
                    model_path,
                    dataset,
                    numeric_columns)

                best, error_df = grid_search(
                    RandomForestRegressor,
                    grid_parameters=grid_parameters,
                    x_train=x_train,
                    y_train=y_train,
                    x_test=x_test,
                    y_test=y_test)

                error_df.to_csv(create_path_if_not_exists(model_path, filename=f'grid_search.csv'), index=False)

                model = RandomForestRegressor(**best)
                model.fit(x_train, y_train)

                save_model(model, model_path=model_path, file_name='rft.pickle')

                save_report(
                    model_path=model_path,
                    train_keys=train_keys,
                    test_keys=test_keys,
                    x_train=x_train,
                    y_train=y_train,
                    x_test=x_test,
                    y_test=y_test,
                    model=model,
                )


if __name__ == '__main__':
    train_tree()
