from utils.aggrecation_utils import aggregate
from typehint.datatype import AggregationMode
from controllers.database import load_database, load_numeric_column_names
import pandas as pd


def feature_correlation(agg_mode: AggregationMode, feature: str):
    sales_df = load_database()

    keys = [
        'seller_id',
        'product_category_name',
        'customer_state',
        'product_id',
    ]

    sales_df = aggregate(sales_df, agg_mode, keys, agg_func='mean', date_col='date')

    numeric_columns = load_numeric_column_names()

    features_corr: pd.DataFrame =  sales_df[numeric_columns].corr().loc[[feature]]

    features_corr = features_corr.drop(columns=[feature])

    features_corr = features_corr.T

    features_corr = features_corr.reset_index()
    features_corr = features_corr.rename(columns={'index': 'features'})

    return features_corr

