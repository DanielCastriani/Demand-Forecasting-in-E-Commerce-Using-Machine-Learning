from pyspark.sql.types import IntegerType, StringType, StructField, StructType

seller_schema = StructType([
    StructField('seller_id', StringType()),
    StructField('seller_zip_code_prefix', IntegerType()),
    StructField('seller_city', StringType()),
    StructField('seller_state', StringType()),
])
