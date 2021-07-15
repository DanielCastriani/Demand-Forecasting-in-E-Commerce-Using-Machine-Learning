from pyspark.sql.types import DateType, StringType, StructField, StructType

order_schema = StructType([
    StructField('order_id', StringType()),
    StructField('customer_id', StringType()),
    StructField('order_status', StringType()),
    StructField('order_purchase_timestamp', DateType()),
    StructField('order_approved_at', DateType()),
    StructField('order_delivered_carrier_date', DateType()),
    StructField('order_delivered_customer_date', DateType()),
    StructField('order_estimated_delivery_date', DateType()),
])
