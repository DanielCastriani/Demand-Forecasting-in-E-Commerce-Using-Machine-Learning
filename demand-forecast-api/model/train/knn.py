
from feature_engineering.make_features import make_features
from utils.loggin_utils import timer
from utils.dataset_utils import load_dataset

import pandas as pd
pd.options.display.max_columns = None

def train_knn():

    date = '2019-01-01'

    with timer(loggin_name='train', message_prefix='train_knn'):
        dataset = load_dataset()

        dataset = make_features(dataset)
