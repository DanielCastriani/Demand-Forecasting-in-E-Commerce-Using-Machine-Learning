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


def calc_order_data_feature(orders: DataFrame):
    orders = orders.withColumnRenamed('order_purchase_timestamp', 'date')

    orders = orders\
        .withColumn('days_to_approve', F.datediff(orders.order_approved_at, orders.date))\
        .withColumn('days_to_post', F.datediff(orders.order_delivered_carrier_date, orders.date))\
        .withColumn('days_to_deliver', F.datediff(orders.order_delivered_customer_date, orders.date))\
        .withColumn('days_estimated_to_deliver', F.datediff(orders.order_estimated_delivery_date, orders.date))

    orders = orders.withColumn('estimated_delivered_diff', orders.days_estimated_to_deliver - orders.days_to_deliver)

    orders = orders.withColumn('is_delayed', orders.estimated_delivered_diff < 0)

    orders = orders.drop(
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date',
    )

    return orders


def filter_order(orders: DataFrame):
    orders = orders.where(~orders.order_status.isin(['canceled', 'unavailable']))

    return orders


def merge_data(
        customers: DataFrame,
        orders: DataFrame,
        order_items: DataFrame,
        products: DataFrame,
        sellers: DataFrame,
        ipca: DataFrame,
        dollar: DataFrame):

    dataset = orders.join(order_items, on=['order_id'])
    dataset = dataset.join(products, on=['product_id'])
    dataset = dataset.join(customers, on=['customer_id'])
    dataset = dataset.join(sellers, on=['seller_id'])
    dataset = dataset.join(dollar, on=['date'])

    dataset = dataset.withColumn('y', F.year(dataset.date))
    dataset = dataset.withColumn('m', F.month(dataset.date))

    dataset = dataset.join(ipca, on=['y', 'm'])

    return dataset
