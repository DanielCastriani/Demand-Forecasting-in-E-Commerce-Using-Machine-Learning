
from dtos.eda_dto import FeatureSummaryDTO, DatasetInfoSummary
from controllers.database import load_database

# TODO remover
import pandas as pd
pd.set_option('display.max_columns', None)


def stats_info():
    sales_df = load_database()

    profit = sales_df['price'] * sales_df['qty']

    mean_product_profit = profit.mean()
    total_profit = profit.sum()

    infos = DatasetInfoSummary(
        mean_product_qty=sales_df['qty'].mean(),
        total_qty=sales_df['qty'].sum(),

        mean_days_to_approve=sales_df['days_to_approve'].mean(),

        mean_days_to_post=sales_df['days_to_post'].mean(),
        min_days_to_post=sales_df[sales_df['days_to_post'] > -1]['days_to_post'].min(),
        max_days_to_post=sales_df['days_to_post'].max(),

        mean_days_to_deliver=sales_df['days_to_deliver'].mean(),
        min_days_to_deliver=sales_df[sales_df['days_to_deliver'] > -1]['days_to_deliver'].min(),
        max_days_to_deliver=sales_df['days_to_deliver'].max(),

        mean_days_estimated_to_deliver=sales_df['days_estimated_to_deliver'].mean(),
        min_days_estimated_to_deliver=sales_df[sales_df['days_estimated_to_deliver'] > -1]['days_estimated_to_deliver'].min(),
        max_days_estimated_to_deliver=sales_df['days_estimated_to_deliver'].max(),

        total_profit=total_profit,
        mean_product_profit=mean_product_profit,
    )

    return infos


def feature_count(agg: int, feature: str):
    sales_df = load_database()

    if agg == -1:
        df = sales_df[feature].value_counts()
        df.index.name = feature

    elif agg == 1:
        df = sales_df.groupby(['customer_city'])[feature].nunique()

    elif agg == 2:
        df = sales_df.groupby(['customer_state'])[feature].nunique()

    df.name = 'count'

    df = df.reset_index()
    df = df.sort_values('count', ascending=False)

    summary = FeatureSummaryDTO(
        rows=len(df),
        df=df,
        nunique=sales_df[feature].nunique()
    )

    return summary


def customer_summary(agg: int):
    sales_df = load_database()

    if agg == 1:
        customers = sales_df.groupby(['customer_city'])['customer_id'].nunique()
    elif agg == 2:
        customers = sales_df.groupby(['customer_state'])['customer_id'].nunique()

    customers = customers.reset_index()
    customers = customers.sort_values('customer_id', ascending=False)

    summary = FeatureSummaryDTO(
        rows=len(customers),
        df=customers,
        nunique=sales_df['customer_id'].nunique()
    )

    return summary


def seller_summary(agg: int):
    sales_df = load_database()

    if agg == 1:
        sellers = sales_df.groupby(['seller_city'])['seller_id'].nunique()
    elif agg == 2:
        sellers = sales_df.groupby(['seller_state'])['seller_id'].nunique()

    sellers = sellers.reset_index()
    sellers = sellers.sort_values('seller_id', ascending=False)

    summary = FeatureSummaryDTO(
        rows=len(sellers),
        df=sellers,
        nunique=sales_df['seller_id'].nunique()
    )

    return summary
