
from typing import List

import pandas as pd

from dtos.report_dtos import ReportDTO, ReportItem
from services.request_service import make_request_json
from typehint.datatype import ListItem
import dash_html_components as html


def load_model_list():
    response = make_request_json('report_list')
    if response['success']:
        body: List[ReportItem] = response['body']

        names = []

        for item in body:
            name = item['name'].split('_')[0]
            keys = ' - '.join([' '.join(c.split('_')) for c in item['keys']]).title()
            agg = item['agg_mode'].upper()

            names.append(ListItem(
                label=f'{name} [{agg}] - {keys}',
                value=item['name']
            ))

        return response['success'], names
    else:
        return response['success'], response.get('message', 'error making request')


def get_report(model_name: str,
               is_delayed: str,
               order_status: str,
               product_category_name: str,
               seller_id: str,
               datatype: str,
               ):
    response = make_request_json(f'report', method='POST', body={
        'model_name': model_name,
        'is_delayed': is_delayed if is_delayed else -1,
        'order_status': order_status if order_status else -1,
        'product_category_name': product_category_name if product_category_name else -1,
        'seller_id': seller_id if seller_id else -1,
        'datatype': datatype if datatype else -1,
    })

    if response['success']:
        body: ReportDTO = response['body']

        df = pd.DataFrame(body['data'])
        filters = body['filters']

        return response['success'], df, filters
    else:
        return response['success'], response.get('message', 'error making request')
