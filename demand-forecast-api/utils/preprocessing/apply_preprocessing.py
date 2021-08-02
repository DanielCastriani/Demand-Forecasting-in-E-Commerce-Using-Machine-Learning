from typing import List
from utils.preprocessing.normalizer import normalizer
from utils.preprocessing.one_hot_encode import one_hot_encoder
from typehint.config_types import FeatureConfigs
import pandas as pd


def apply_preprocessing(
        df: pd.DataFrame,
        config: FeatureConfigs,
        numeric_columns: List[str],
        model_path: str,
        train: bool):

    numeric_columns = [c for c in numeric_columns if c != config['target']]

    df, keys_df, one_hot_cols = one_hot_encoder(df, keys=config['keys'], path=model_path, train=train)
    df, normalized_cols = normalizer(df, columns=numeric_columns, path=model_path, train=train)

    if config['date_column'] in df.columns:
        keys_df['date'] = df[config['date_column']]
        df = df.drop(columns=[config['date_column']])

    if 'product_id' in df.columns:
        df = df.drop(columns=['product_id'])

    return df, one_hot_cols, normalized_cols, keys_df
