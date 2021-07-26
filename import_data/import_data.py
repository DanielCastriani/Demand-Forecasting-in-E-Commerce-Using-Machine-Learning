
import os

from dataset.external_data import load_dollar, load_ipca
from utils.sys_command import run_cmd

file_path_folder = 'data/'

filename_list = [
    'olist_orders_dataset.csv',
    'olist_order_items_dataset.csv',
    'olist_customers_dataset.csv',
    'olist_products_dataset.csv',
    'olist_sellers_dataset.csv',
    'ipca.csv',
    'dollar.csv',
]

ipca = load_ipca(path=file_path_folder)
dollar = load_dollar(path=file_path_folder)

ipca_path = os.path.join(file_path_folder, 'ipca.csv')
dollar_path = os.path.join(file_path_folder, 'dollar.csv')

ipca.to_csv(ipca_path, index=False)
dollar.to_csv(dollar_path, index=False)

run_cmd(["hdfs", "dfs", "-mkdir", 'dataset'])

for filename in filename_list:

    local_path = os.path.join(file_path_folder, filename)
    local_path = os.path.abspath(local_path)

    hdfs_path = os.path.join(os.sep, 'user', 'daniel', 'dataset', filename)

    run_cmd(["hdfs", "dfs", "-put", local_path, hdfs_path])
