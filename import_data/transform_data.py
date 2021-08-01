from pyspark import SparkContext
from pyspark.sql import SparkSession

from schemas import customer_schema, dollar_schema, ipca_schema, order_item_schema, order_schema, product_schema, seller_schema
from utils.feature_engineering_utils import calc_order_data_feature, filter_order, group_order_items, merge_data

master = 'spark://hadoop:7077'
appName = 'Transform Data'
hdfs_path = 'hdfs://hadoop:9000/user/daniel/dataset/{}'

sc = SparkContext(master=master, appName=appName)
spark = SparkSession.builder.appName(appName).master(master).getOrCreate()


customers = spark.read.csv(hdfs_path.format('olist_customers_dataset.csv'), header=True, schema=customer_schema)
orders = spark.read.csv(hdfs_path.format('olist_orders_dataset.csv'), header=True, schema=order_schema)
order_items = spark.read.csv(hdfs_path.format('olist_order_items_dataset.csv'), header=True, schema=order_item_schema)
products = spark.read.csv(hdfs_path.format('olist_products_dataset.csv'), header=True, schema=product_schema)
sellers = spark.read.csv(hdfs_path.format('olist_sellers_dataset.csv'), header=True, schema=seller_schema)

ipca = spark.read.csv(hdfs_path.format('ipca.csv'), header=True, schema=ipca_schema)
dollar = spark.read.csv(hdfs_path.format('dollar.csv'), header=True, schema=dollar_schema)


order_items = group_order_items(order_items)

orders = filter_order(orders)

orders = calc_order_data_feature(orders)

dataset = merge_data(customers, orders, order_items, products, sellers, ipca, dollar)

dataset = dataset.dropna(subset=[
    'product_category_name',
    'product_name_lenght',
    'product_description_lenght',
    'product_photos_qty',
    'product_weight_g',
    'product_length_cm',
    'product_height_cm',
    'product_width_cm',
])

dataset.where(dataset.days_to_deliver == 0).toPandas()

dataset = dataset.fillna(-1, subset=[
    'days_to_approve',
    'days_to_post',
    'days_to_deliver',
    'estimated_delivered_diff',
])

dataset = dataset.fillna(False, subset=['is_delayed'])

dataset.repartition(1).write.mode('overwrite').parquet(hdfs_path.format('dataset.parquet'))

categories = products.select(products.product_category_name).distinct()

categories = categories.dropna(subset=['product_category_name'])

categories.repartition(1).write.mode('overwrite').parquet(hdfs_path.format('categories.parquet'))
