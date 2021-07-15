from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def group_order_items(order_items: DataFrame):
    keys = ['order_id', 'product_id', 'seller_id']

    order_items = order_items.groupBy(keys).agg(
        F.count('product_id'),
        F.sum('price'),
        F.sum('freight_value'),
    )

    order_items = order_items\
        .withColumnRenamed('count(product_id)', 'qty')\
        .withColumnRenamed('sum(price)', 'price')\
        .withColumnRenamed('sum(freight_value)', 'freight_value')

    order_items = order_items.withColumn('price', order_items.price/order_items.qty)
    order_items = order_items.withColumn('total', order_items.price + order_items.freight_value)

    return order_items
