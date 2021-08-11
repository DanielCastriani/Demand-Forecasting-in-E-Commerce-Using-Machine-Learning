from typehint.config_types import FeatureConfigs, LagConfig

_target_column = 'qty'

_lag_w = [
    LagConfig(start=1, end=54, steps=1, column=_target_column),
    LagConfig(start=1, end=16, steps=1, column='days_to_approve'),
    LagConfig(start=1, end=24, steps=1, column='days_to_post'),
    LagConfig(start=1, end=24, steps=1, column='days_to_deliver'),
    LagConfig(start=1, end=24, steps=1, column='days_estimated_to_deliver'),
    LagConfig(start=1, end=24, steps=1, column='estimated_delivered_diff'),
    LagConfig(start=1, end=54, steps=1, column='price'),
    LagConfig(start=1, end=54, steps=1, column='freight_value'),
    LagConfig(start=1, end=54, steps=1, column='total'),
    LagConfig(start=1, end=24, steps=1, column='product_name_lenght'),
    LagConfig(start=1, end=24, steps=1, column='product_description_lenght'),
    LagConfig(start=1, end=24, steps=1, column='product_photos_qty'),
    LagConfig(start=1, end=24, steps=1, column='product_weight_g'),
    LagConfig(start=1, end=24, steps=1, column='product_length_cm'),
    LagConfig(start=1, end=24, steps=1, column='product_height_cm'),
    LagConfig(start=1, end=24, steps=1, column='product_width_cm'),
    LagConfig(start=1, end=54, steps=1, column='dollar'),
    LagConfig(start=1, end=54, steps=1, column='ipca'),
]

_lag_m = [
    LagConfig(start=1, end=12, steps=1, column=_target_column),
    LagConfig(start=1, end=4, steps=1, column='days_to_approve'),
    LagConfig(start=1, end=6, steps=1, column='days_to_post'),
    LagConfig(start=1, end=6, steps=1, column='days_to_deliver'),
    LagConfig(start=1, end=6, steps=1, column='days_estimated_to_deliver'),
    LagConfig(start=1, end=6, steps=1, column='estimated_delivered_diff'),
    LagConfig(start=1, end=12, steps=1, column='price'),
    LagConfig(start=1, end=12, steps=1, column='freight_value'),
    LagConfig(start=1, end=12, steps=1, column='total'),
    LagConfig(start=1, end=6, steps=1, column='product_name_lenght'),
    LagConfig(start=1, end=6, steps=1, column='product_description_lenght'),
    LagConfig(start=1, end=6, steps=1, column='product_photos_qty'),
    LagConfig(start=1, end=6, steps=1, column='product_weight_g'),
    LagConfig(start=1, end=6, steps=1, column='product_length_cm'),
    LagConfig(start=1, end=6, steps=1, column='product_height_cm'),
    LagConfig(start=1, end=6, steps=1, column='product_width_cm'),
    LagConfig(start=1, end=12, steps=1, column='dollar'),
    LagConfig(start=1, end=12, steps=1, column='ipca'),
]

_key_1 = ['product_category_name', 'order_status', 'is_delayed']
_key_2 = ['product_category_name', 'product_id', 'order_status', 'is_delayed']

_values = [
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
    'ipca'
]

_date_column = 'date'

config_w_1 = FeatureConfigs(
    name='w_1',
    agg_mode='w',
    keys=_key_1,
    values=_values,
    date_column=_date_column,
    target=_target_column,
    lag_config=_lag_w

)

config_w_2 = FeatureConfigs(
    name='w_2',
    agg_mode='w',
    keys=_key_2,
    values=_values,
    date_column=_date_column,
    target=_target_column,
    lag_config=_lag_w

)

config_m_1 = FeatureConfigs(
    name='m_1',
    agg_mode='m',
    keys=_key_1,
    values=_values,
    date_column=_date_column,
    target=_target_column,
    lag_config=_lag_m

)

config_m_2 = FeatureConfigs(
    name='m_2',
    agg_mode='m',
    keys=_key_2,
    values=_values,
    date_column=_date_column,
    target=_target_column,
    lag_config=_lag_m

)

config_list = [
    config_m_1,
    config_m_2,
    config_w_1,
    config_w_2,
]
