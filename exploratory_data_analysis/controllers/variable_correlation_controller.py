from utils.lag_feature import lag_columns, lag_feature
from utils.aggrecation_utils import aggregate
from typehint.datatype import AggregationMode
from controllers.database import load_database, load_numeric_column_names
import pandas as pd


keys = [
    'seller_id',
    'product_category_name',
    'customer_state',
    'product_id',
]


def feature_correlation(agg_mode: AggregationMode, feature: str):
    sales_df = load_database()

    sales_df = aggregate(sales_df, agg_mode, keys, agg_func='mean', date_col='date')

    numeric_columns = load_numeric_column_names()

    features_corr: pd.DataFrame = sales_df[numeric_columns].corr().loc[[feature]]

    features_corr = features_corr.drop(columns=[feature])

    features_corr = features_corr.T

    features_corr = features_corr.reset_index()
    features_corr = features_corr.rename(columns={'index': 'features'})

    return features_corr


def lag_correlation(agg_mode: AggregationMode, feature_column: str, lag_feature_column: str, window: int):
    sales_df = load_database()
    sales_df = sales_df[set(['date', *keys, feature_column, lag_feature_column])]

    if feature_column == lag_feature_column:
        sales_df[f'{feature_column}(A)'] = sales_df[feature_column]
        sales_df[f'{lag_feature_column}(B)'] = sales_df[lag_feature_column]
        
        feature_column = f'{feature_column}(A)'
        lag_feature_column = f'{lag_feature_column}(B)'


    sales_df = sales_df.sort_values('date')

    sales_df = aggregate(sales_df, agg_mode, keys, agg_func='mean', date_col='date')

    df = lag_feature(
        df=sales_df,
        keys=keys,
        column=lag_feature_column,
        window=window)

    df = df[lag_columns(df, lag_feature_column, ext=[feature_column])]

    corr = df.corr()

    corr: pd.DataFrame = corr[[feature_column]].iloc[: -1].reset_index()

    return corr.rename(columns={'index': lag_feature_column})
