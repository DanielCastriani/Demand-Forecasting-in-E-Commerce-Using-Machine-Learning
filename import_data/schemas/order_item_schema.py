from pyspark.sql.types import IntegerType, StringType, StructField, StructType, DateType, FloatType


order_item_schema = StructType([
    StructField('order_id', StringType()),
    StructField('order_item_id', IntegerType()),
    StructField('product_id', StringType()),
    StructField('seller_id', StringType()),
    StructField('shipping_limit_date', DateType()),
    StructField('price', FloatType()),
    StructField('freight_value', FloatType()),
])
