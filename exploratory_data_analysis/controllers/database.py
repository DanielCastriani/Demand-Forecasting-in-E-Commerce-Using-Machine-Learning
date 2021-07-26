import pandas as pd

url = 'hdfs://hadoop:9000/user/daniel/dataset'


def load_database():
    dataset_path = f'{url}/dataset.parquet'
    df = pd.read_parquet(dataset_path)

    df['date'] = pd.to_datetime(df['date'])

    return df


def load_category():

    dataset_path = f'{url}/subcategories.parquet'
    df = pd.read_parquet(dataset_path)

    return df


def load_column_names():
    return [
        'y',
        'm',
        'date',
        'seller_id',
        'customer_id',
        'product_id',
        'order_id',
        *load_numeric_column_names(),
        *load_categorical_column_names()
    ]


def load_numeric_column_names():
    return [
        'qty',
        'days_to_approve',
        'days_to_post',
        'days_to_deliver',
        'days_estimated_to_deliver',
        'estimated_delivered_diff',
        'price',
        'freight_value',
        'total',
        'product_name_lenght',
        'product_description_lenght',
        'product_photos_qty',
        'product_weight_g',
        'product_length_cm',
        'product_height_cm',
        'product_width_cm',
        'dollar',
        'ipca',
    ]


def load_categorical_column_names():
    return [
        'customer_unique_id',
        'customer_zip_code_prefix',
        'customer_city',
        'customer_state',
        'seller_zip_code_prefix',
        'seller_city',
        'seller_state',
        'order_status',
        'is_delayed',
        'product_category_name'
    ]
