from pyspark.sql.types import DateType, FloatType, StructField, StructType

dollar_schema = StructType([
    StructField('date', DateType()),
    StructField('dollar', FloatType()),
])
