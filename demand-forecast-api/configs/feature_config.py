from typehint.config_types import LagConfig

KEYS = [
    # 'seller_state',
    'product_category_name',
    # 'product_id',
    'order_status',
    'is_delayed',
]

VALUES = [
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

DATE_COLUMN = 'date'

TARGET = 'qty'

AGG_MODE = 'w'

LAG_CONFIG = [
    LagConfig(start=1, end=54, steps=1, column=TARGET),
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
