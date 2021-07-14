import json
import os

import requests

from utils.file_utils import mkdir_if_not_exists


def download_json_if_not_exist(
        url: str, file_name: str, path: str = 'data/', override: bool = False, verbose: bool = True):
    file_path = os.path.join(mkdir_if_not_exists(path), file_name)

    if not os.path.exists(file_path) or override:
        if verbose:
            print(f'Downloading: {url}')
        response = requests.get(url)
        dollar = response.json()

        with open(file_path, 'w') as f:
            json.dump(dollar, f)

    with open(file_path, 'r') as f:
        return json.load(f)
