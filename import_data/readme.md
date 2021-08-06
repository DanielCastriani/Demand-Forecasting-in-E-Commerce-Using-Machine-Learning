To import data, you need to start hdfs and spark. And you also need to create a folter data/ on root foldert of import_data project, and paste all csvs from the links below. All other data will be downloaded aultimaticaly.

- https://www.kaggle.com/olistbr/brazilian-ecommerce
- https://www.kaggle.com/olistbr/marketing-funnel-olist

```sh
python import_data.py
python transform_data.py
```