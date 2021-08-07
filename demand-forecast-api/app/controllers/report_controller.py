
from app.controllers import model_controller
from app.utils.df_utils import filter_df
import json
import os

import pandas as pd
from app.dtos.http_response_dto import HTTPResponseDTO
from app.dtos.report_dtos import ReportDTO, RequestReportDTO


def get_report_list():
    path_list = model_controller.model_list()

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



def get_model_performance_report():
    path_list = model_controller.model_list()

    root_path = 'bin/'

    if len(path_list) > 0: 
        df_list = []
        
        for path in path_list:
            df = pd.read_csv(os.path.join(root_path, path['name'], 'erro.csv'))
            df['Model'] = path['name']
            df['ModelType'] = path['name'].split('_')[0]
            df['AggregationMode'] = path['agg_mode']
            df['Granularity'] = ', '.join(path['keys'])
            
            df_list.append(df)
        
        report_df = pd.concat(df_list)
        report_df = report_df.rename(columns={'Unnamed: 0': 'dataset'})

        report_df = report_df.sort_values(['dataset', 'AggregationMode', 'mape'])

        report_df= report_df[['dataset', 'ModelType', 'Model', 'AggregationMode', 'mape', 'mae', 'Granularity']]

        report_dict = report_df.to_dict(orient='records')

        return HTTPResponseDTO(
            body=report_dict,
            success=True,
        )



    return HTTPResponseDTO(
        body=[],
        success=False,
        message='No models found'
    )

    


def get_report_data(body: RequestReportDTO):
    path = os.path.join('bin', body['model_name'], 'results.csv')
    if os.path.exists(path):

        df = pd.read_csv(path)

        config = model_controller.get_config(body['model_name'])
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
