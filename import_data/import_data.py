
from typing import List
from dataset.external_data import load_dollar, load_ipca
import os
import subprocess

env = os.environ.copy()
HADOOP_HOME = '/opt/hadoop'
env['PATH'] = f"{HADOOP_HOME}/bin:{HADOOP_HOME}/sbin:{env['PATH']}"


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


def run_cmd(args_list: List):
    print(f"> {' '.join(args_list)}")
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    s_output, s_err = proc.communicate()
    s_return = proc.returncode
    print(s_output.decode() if s_output else s_err.decode())


for filename in filename_list:

    local_path = os.path.join(file_path_folder, filename)
    local_path = os.path.abspath(local_path)

    hdfs_path = os.path.join(os.sep, 'user', 'daniel', 'dataset', filename)

    run_cmd(["hdfs", "dfs", "-put", local_path, hdfs_path])
