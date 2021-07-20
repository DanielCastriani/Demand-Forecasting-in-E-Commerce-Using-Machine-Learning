from pyspark.sql.types import FloatType, IntegerType, StructField, StructType

ipca_schema = StructType([
    StructField('m', IntegerType()),
    StructField('y', IntegerType()),
    StructField('ipca', FloatType()),
])
