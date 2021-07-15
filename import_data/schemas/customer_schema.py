
from pyspark.sql.types import IntegerType, StringType, StructField, StructType


customer_schema = StructType([
    StructField('customer_id', StringType()),
    StructField('customer_unique_id', StringType()),
    StructField('customer_zip_code_prefix', IntegerType()),
    StructField('customer_city', StringType()),
    StructField('customer_state', StringType()),
])
