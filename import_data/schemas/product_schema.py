

from pyspark.sql.types import IntegerType, StringType, StructField, StructType

product_schema = StructType([
    StructField('product_id', StringType()),
    StructField('product_category_name', StringType()),
    StructField('product_name_lenght', IntegerType()),
    StructField('product_description_lenght', IntegerType()),
    StructField('product_photos_qty', IntegerType()),
    StructField('product_weight_g', IntegerType()),
    StructField('product_length_cm', IntegerType()),
    StructField('product_height_cm', IntegerType()),
    StructField('product_width_cm', IntegerType()),
])
