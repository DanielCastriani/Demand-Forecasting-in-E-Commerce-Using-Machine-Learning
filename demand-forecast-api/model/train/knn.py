
import pandas as pd
from configs.feature_config import config_list
from feature_engineering.make_features import make_features
from sklearn.neighbors import KNeighborsRegressor
from utils.config_utils import get_config
from utils.dataset_utils import load_dataset
from utils.error_report import error_report
from utils.file_utils import create_path_if_not_exists, save_model
from utils.loggin_utils import get_loggin, timer
from utils.model_utils import create_model_folder
from utils.report_utils import save_report
from utils.split_utils import split_pipeline

pd.options.display.max_columns = None


def train_knn():

    test_date = '2018-05-01'

    console = get_loggin()
    console.info(f'N_JOBS: {get_config("N_JOBS")}')

    with timer(loggin_name='train', message_prefix=f'train KNN models'):
        for config in config_list:
            model_name, model_path = create_model_folder(config, regressor_name='KNeighborsRegressor')
            console.info(f'\n\n\n{model_name}')

            with timer(loggin_name='train', message_prefix=f'train {model_name}'):
                dataset = load_dataset()
                dataset, numeric_columns = make_features(dataset, config=config)

                train_keys, test_keys, x_train, y_train, x_test, y_test = split_pipeline(
                    test_date,
                    config,
                    model_path,
                    dataset,
                    numeric_columns)

                error_list = []
                total_k = 30
                for k in range(5, total_k):
                    knn = KNeighborsRegressor(n_neighbors=k, n_jobs=get_config('N_JOBS'))
                    knn.fit(x_train, y_train)

                    predict = knn.predict(x_test)

                    error = error_report(y_test, predict)
                    error_list.append({**error, 'k': k})
                    console.info(f'{k} / {total_k} - {error}')

                error_df = pd.DataFrame(error_list)
                error_df = error_df.sort_values('mape')
                error_df.to_csv(create_path_if_not_exists(model_path, filename=f'{model_name}.csv'), index=False)

                best = error_df.head(1)

                k = best['k'].values[0]
                knn = KNeighborsRegressor(n_neighbors=k, n_jobs=get_config('N_JOBS'))
                knn.fit(x_train, y_train)

                save_model(knn, model_path=model_path, file_name='model.pickle')

                save_report(
                    model_path=model_path,
                    train_keys=train_keys,
                    test_keys=test_keys,
                    x_train=x_train,
                    y_train=y_train,
                    x_test=x_test,
                    y_test=y_test,
                    model=knn,
                )


if __name__ == '__main__':
    train_knn()
