
from app.utils.df_utils import filter_df
import json
import os

import pandas as pd
from app.dtos.http_response_dto import HTTPResponseDTO
from app.dtos.report_dtos import ReportDTO, ReportItem, RequestReportDTO
from typehint.config_types import FeatureConfigs


def get_report_list():
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

        if len(path_list) > 0:
            path_list.sort(key=lambda x: x['name'])

            return HTTPResponseDTO(
                body=path_list,
                success=True,
            )

    return HTTPResponseDTO(
        body=[],
        success=False,
        message='No models found'
    )


def get_config(model_name: str) -> FeatureConfigs:
    config_path = os.path.join('bin', model_name, 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)

    else:
        raise FileNotFoundError('Config file not found')


def get_report_data(body: RequestReportDTO):
    path = os.path.join('bin', body['model_name'], 'results.csv')
    if os.path.exists(path):

        df = pd.read_csv(path)

        config = get_config(body['model_name'])
        config['keys'] = ['type', *[c for c in config['keys'] if c != 'product_id']]

        filters = {c: sorted(df[c].unique().tolist()) for c in config['keys']}

        body['is_delayed'] = bool(body.get('is_delayed')) if body.get('is_delayed') else None

        df = filter_df(df, column='is_delayed', value=body.get('is_delayed', -1))
        df = filter_df(df, column='order_status', value=body.get('order_status', -1))
        df = filter_df(df, column='product_category_name', value=body.get('product_category_name', -1))
        df = filter_df(df, column='seller_id', value=body.get('seller_id', -1))
        df = filter_df(df, column='type', value=body.get('datatype', -1))

        df = df.pivot_table(['real', 'predicted'], index=['date', 'type'], aggfunc='sum')
        df = df.reset_index()

        return HTTPResponseDTO(
            body=ReportDTO(data=df.to_dict(orient='records'), filters=filters),
            success=True
        )

    else:
        return HTTPResponseDTO(
            body=[],
            success=False,
            message='No models found'
        )
