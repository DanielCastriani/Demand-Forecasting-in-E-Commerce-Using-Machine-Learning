import os
from configparser import ConfigParser

from typehint import ConfigType

from utils.file_utils import create_path_if_not_exists


def generate_config_file():
    config = ConfigParser()
    config.optionxform = lambda x: x.upper()

    HDFS_URL = input('hdfs url [hdfs://hadoop:9000/user/daniel/dataset]:') or 'hdfs://hadoop:9000/user/daniel/dataset'
    N_JOBS = input('N_JOBS [5]:') or 5

    N_JOBS = int(N_JOBS)

    config['DEFAULT'] = ConfigType(
        HDFS=HDFS_URL,
        N_JOBS=N_JOBS,
    )

    file_path = create_path_if_not_exists('configs', filename='config.ini')

    with open(file_path, 'w') as f:
        config.write(f)


def get_config_file(key: str = None):
    parser = ConfigParser()
    parser.optionxform = str

    file_path = os.path.join('configs', 'config.ini')

    parser.read(file_path)
    default = dict(parser.items('DEFAULT'))

    configs = ConfigType(**default)
    configs['N_JOBS'] = int(configs['N_JOBS'])

    configs['N_JOBS'] = int(configs.get('N_JOBS', -1))

    if key:
        return configs[key]
    else:
        return configs


def _get_config(config: dict, key: str = None):
    return dict(config) if key is None else config.get(key)

def get_config(key: str = None):
    from flask import current_app
    try:
        return _get_config(current_app.config, key)
    except:
        from server import app
        with app.app_context():
            return _get_config(current_app.config, key)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Configuration utils')

    generate = parser.add_mutually_exclusive_group()
    generate.add_argument('-g', '--generate', action='store_true', help='Generate a config file')

    args = parser.parse_args()

    if args.generate:
        generate_config_file()
