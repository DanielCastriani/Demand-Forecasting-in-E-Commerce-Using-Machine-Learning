from schemas import order_item_schema, order_schema, customer_schema, product_schema, seller_schema
from pyspark import SparkContext
from pyspark.sql import SparkSession


master = 'spark://127.0.1.1:7077'
appName = 'Transform Data'

sc = SparkContext(master=master, appName=appName)
spark = SparkSession.builder.appName(appName).master(master).getOrCreate()


file_path = 'hdfs://localhost:9000/user/daniel/dataset/{}'


customers = spark.read.csv(file_path.format('olist_customers_dataset.csv'), header=True, schema=customer_schema)
orders = spark.read.csv(file_path.format('olist_orders_dataset.csv'), header=True, schema=order_schema)
order_items = spark.read.csv(file_path.format('olist_order_items_dataset.csv'), header=True, schema=order_item_schema)
products = spark.read.csv(file_path.format('olist_products_dataset.csv'), header=True, schema=product_schema)
sellers = spark.read.csv(file_path.format('olist_sellers_dataset.csv'), header=True, schema=seller_schema)
