import os, json
from typing import List
from app.dtos.report_dtos import ReportItem

def model_list() -> List[ReportItem]:
    path = 'bin'
    if os.path.exists(path):
        path_list = []
        for entry in os.scandir(path):

            config_path = os.path.join(entry.path, 'config.json')
            with open(config_path, 'r') as f:
                model_config = json.load(f)

            granularity = model_config['keys']
            agg_mode = model_config['agg_mode']

            path_list.append(ReportItem(name=entry.name, keys=granularity, agg_mode=agg_mode))

        return path_list
    return []