from utils.filter_utils import filter_df
from utils.normalizer import normalize
from utils.lag_feature import lag_columns, lag_feature
from utils.aggrecation_utils import aggregate, join_date
from typehint.datatype import AggregationMode
from controllers.database import load_database, load_numeric_column_names
import pandas as pd


keys = [
    'seller_id',
    'product_category_name',
    'customer_state',
    'product_id',
]


def feature_correlation(agg_mode: AggregationMode, feature: str, category: str):
    sales_df = load_database()
    sales_df = filter_df(sales_df, 'product_category_name', category)

    sales_df = aggregate(sales_df, agg_mode, keys, agg_func='mean', date_col='date')

    numeric_columns = load_numeric_column_names()

    features_corr: pd.DataFrame = sales_df[numeric_columns].corr().loc[[feature]]

    features_corr = features_corr.drop(columns=[feature])

    features_corr = features_corr.T

    features_corr = features_corr.reset_index()
    features_corr = features_corr.rename(columns={'index': 'features'})

    return features_corr


def lag_correlation(agg_mode: AggregationMode, feature_column: str, lag_feature_column: str, category: str, window: int):
    sales_df = load_database()
    sales_df = filter_df(sales_df, 'product_category_name', category)

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


def mean_by_cat_date(agg_mode: AggregationMode, feature_column: str, category: str, is_compare: bool):
    sales_df = load_database()

    sales_df = filter_df(sales_df, 'product_category_name', category)

    sales_df = sales_df.sort_values('date')

    agg_keys = [
        'product_category_name'
    ] if is_compare else []

    sales_df = sales_df[[*agg_keys, 'date', feature_column]]
    agg_func = 'sum' if feature_column == 'qty' else 'mean'

    sales_df = aggregate(sales_df, agg_mode, agg_keys, agg_func=agg_func, date_col='date')

    sales_df = join_date(sales_df, agg_mode)

    return sales_df


def ext_data_x_feature(agg_mode: AggregationMode, var_col: str, category: str, is_normalize: bool):
    sales_df = load_database()

    sales_df = filter_df(sales_df, 'product_category_name', category)

    sales_df = sales_df[['date', var_col, 'dollar', 'ipca']]

    if var_col == 'qty':
        sales_df_sum = aggregate(sales_df[['date', var_col]], agg_mode, [], agg_func='sum', date_col='date')
        sales_df_sum = join_date(sales_df_sum, agg_mode=agg_mode)

        sales_df_mean = aggregate(sales_df[['date', 'dollar', 'ipca']], agg_mode, [], agg_func='mean', date_col='date')
        sales_df_mean = join_date(sales_df_mean, agg_mode=agg_mode)

        sales_df_mean = sales_df_mean.merge(sales_df_sum, on=['date'])

    else:
        sales_df_mean = aggregate(sales_df, agg_mode, [], agg_func='mean', date_col='date')
        sales_df_mean = join_date(sales_df_mean, agg_mode=agg_mode)


    if is_normalize:
        for col in [var_col, 'dollar', 'ipca']:
            c_min = sales_df_mean[col].min()
            d = sales_df_mean[col].max() - c_min
            sales_df_mean[col] = (sales_df_mean[col] - c_min) / d

    return sales_df_mean
