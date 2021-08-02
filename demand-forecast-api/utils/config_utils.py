import os
from configparser import ConfigParser
from typing import Literal

from typehint import ConfigType

from utils.file_utils import create_path_if_not_exists


def generate_config_file():
    config = ConfigParser()

    hdfs_url = input('hdfs url [hdfs://hadoop:9000/user/daniel/dataset]:') or 'hdfs://hadoop:9000/user/daniel/dataset'
    n_jobs = input('N_JOBS [5]:') or 5

    n_jobs = int(n_jobs)

    config['DEFAULT'] = ConfigType(
        hdfs=hdfs_url,
        n_jobs=n_jobs,
    )

    file_path = create_path_if_not_exists('configs', filename='config.ini')

    with open(file_path, 'w') as f:
        config.write(f)


def get_configs(key: str = None):
    parser = ConfigParser()

    file_path = os.path.join('configs', 'config.ini')

    parser.read(file_path)
    default = dict(parser.items('DEFAULT'))

    configs = ConfigType(**default)

    configs['n_jobs'] = int(configs.get('n_jobs', -1))

    if key:
        return configs[key]
    else:
        return configs


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Configuration utils')

    generate = parser.add_mutually_exclusive_group()
    generate.add_argument('-g', '--generate', action='store_true', help='Generate a config file')

    args = parser.parse_args()

    if args.generate:
        generate_config_file()
