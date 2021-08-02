
import pandas as pd
from configs.feature_config import KEYS, TARGET
from feature_engineering.make_features import make_features
from sklearn.neighbors import KNeighborsRegressor
from utils.dataset_utils import load_dataset
from utils.error_report import error_report
from utils.file_utils import create_path_if_not_exists
from utils.loggin_utils import timer
from utils.preprocessing.normalizer import normalizer
from utils.preprocessing.one_hot_encode import one_hot_encoder
from utils.split_utils import split_train_test_timeseries, split_x_y

pd.options.display.max_columns = None


def train_knn():

    test_date = '2018-05-01'

    with timer(loggin_name='train', message_prefix='train_knn'):
        dataset = load_dataset()
        dataset, numeric_columns = make_features(dataset)

        train, test = split_train_test_timeseries(dataset, test_date=test_date, verbose=True)

        train, _ = one_hot_encoder(train, keys=KEYS, train=True)
        train, _ = normalizer(train, columns=numeric_columns, train=True)

        test, _ = one_hot_encoder(test, keys=KEYS, train=False)
        test, _ = normalizer(test, columns=numeric_columns, train=False)

        x_train, y_train = split_x_y(train, TARGET)
        x_test, y_test = split_x_y(test, TARGET)

        error_list = []
        for k in range(5, 500):
            knn = KNeighborsRegressor(n_neighbors=k, n_jobs=6)
            knn.fit(x_train, y_train)

            predict = knn.predict(x_test)

            error = error_report(y_test, predict)

            error_list.append({**error, 'k': k})

        error_df = pd.DataFrame(error_list)

        error_df = error_df.sort_values('mape')

        error_df.to_csv(create_path_if_not_exists('logs', filename='knn_error.csv'), index=False)
