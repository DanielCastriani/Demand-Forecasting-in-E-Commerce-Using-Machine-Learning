# Demand-Forecasting-in-E-Commerce-Using-Machine-Learning
Demand forecasting is essential for making decisions to make a store more competitive. A store can lose money because it has an excessive stock of a certain product, or failing to sell a certain product due to lack of stock. Due to the number of factors that can influence this forecast, it is necessary to use machine learning to increase accuracy. The project aims to forecast demand for an e-commerce, testing various machine learning algorithms.

# Install Hadoop
* [0 - Prepare Environment](./doc/0_prepare_environment.md)
* [1 - Install Hadoop](./doc/1_install_hadoop.md)
* [2 - Install Spark](./doc/2_install_spark.md)

# Initialize Hadoop

```
start-dfs.sh
/opt/spark/sbin/start-master.sh
/opt/spark/sbin/start-slave.sh spark://192.168.2.100:7077
```

# Create folders

```bash

hdfs dfs -mkdir /user
hdfs dfs -mkdir /user/hadoop
hdfs dfs -mkdir /user/daniel
hdfs dfs -chown daniel /user/daniel

# with user daniel
hdfs dfs -mkdir /user/daniel/dataset

```

[hdfs](http://localhost:9870/)

[yarn](http://localhost:8088/)

[spark](http://localhost:8080/)

Before run the projects, you will need to import data by running scripts from import_data projects. You will need to read the [import_data](import_data/README.md) documentation.

## Datasets

- https://www.kaggle.com/olistbr/brazilian-ecommerce
- https://www.kaggle.com/olistbr/marketing-funnel-olist
- https://sidra.ibge.gov.br/tabela/1737 [IPCA - Número-índice (base: dezembro de 1993 = 100)]
- https://dadosabertos.bcb.gov.br/dataset/10813-taxa-de-cambio---livre---dolar-americano-compra


## Data Dictionary

| Column                          |                             Description                              |                        Source |
| :------------------------------ | :------------------------------------------------------------------: | ----------------------------: |
| order_id                        |                   Unique identifier of the order.                    |      olist_orders_dataset.csv |
| customer_id                     |                             Customer id.                             |      olist_orders_dataset.csv |
| order_status                    |                Order status (delivered, shipped,... )                |      olist_orders_dataset.csv |
| date [order_purchase_timestamp] |                            Purchase date                             |      olist_orders_dataset.csv |
| order_approved_at               |                       Order purchase datetime                        |      olist_orders_dataset.csv |
| order_delivered_carrier_date    |                        Order posting datetime                        |      olist_orders_dataset.csv |
| order_delivered_customer_date   |                      Actual order delivery date                      |      olist_orders_dataset.csv |
| order_estimated_delivery_date   |                       Estimated delivery date                        |      olist_orders_dataset.csv |
| order_item_id                   |                               Order id                               | olist_order_items_dataset.csv |
| product_id                      |                              Product id                              | olist_order_items_dataset.csv |
| seller_id                       |                              Seller id                               | olist_order_items_dataset.csv |
| shipping_limit_date             |                            Shipping limit                            | olist_order_items_dataset.csv |
| price                           |                            Product price                             | olist_order_items_dataset.csv |
| freight_value                   | Freight price. If order has more then on item, the price is splited. | olist_order_items_dataset.csv |
| product_category_name           |                       Category of ther product                       |    olist_products_dataset.csv |
| product_name_lenght             |        Number of characters extracted from the product name.         |    olist_products_dataset.csv |
| product_description_lenght      |     Number of characters extracted from the product description      |    olist_products_dataset.csv |
| product_photos_qty              |                  Number of product published photos                  |    olist_products_dataset.csv |
| product_weight_g                |                         Product weight in g                          |    olist_products_dataset.csv |
| product_length_cm               |                         product lenght in cm                         |    olist_products_dataset.csv |
| product_height_cm               |                         product height in cm                         |    olist_products_dataset.csv |
| product_width_cm                |                         product width in cm                          |    olist_products_dataset.csv |
| customer_unique_id              |                             Customer Id                              |   olist_customers_dataset.csv |
| customer_zip_code_prefix        |                  Customer Zip code. First 5 numbers                  |   olist_customers_dataset.csv |
| customer_city                   |                            Customer City                             |   olist_customers_dataset.csv |
| customer_state                  |                             Customer Uf                              |   olist_customers_dataset.csv |
| seller_zip_code_prefix          |                   Seller Zip code. First 5 numbers                   |     olist_sellers_dataset.csv |
| seller_city                     |                             Seller City.                             |     olist_sellers_dataset.csv |
| seller_state                    |                              Seller UF.                              |     olist_sellers_dataset.csv |
| y                               |                            Purchase year                             |      order_purchase_timestamp |
| m                               |                            Purchase month                            |      order_purchase_timestamp |
| ipca                            |     National consumer price index. Brazil's main inflation index     |             sidra.ibge.gov.br |
| dollar                          |                        Dollar quote in Real.                         |       dadosabertos.bcb.gov.br |
