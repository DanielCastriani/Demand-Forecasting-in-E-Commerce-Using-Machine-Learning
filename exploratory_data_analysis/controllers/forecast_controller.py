

import pandas as pd
from dtos.http_response_dto import HTTPResponseDTO
from services.request_service import make_request_json
from dtos.forecast_dtos import ForecastRequestDTO, ForecastResponseDTO


def make_forecast(
    model_name: str,
    is_delayed: str,
    order_status: str,
    product_category_name: str,
    seller_id: str,
    datatype: str,
    window_size: int
):
    body = ForecastRequestDTO(
        is_delayed=is_delayed,
        model_name=model_name,
        order_status=order_status,
        product_category_name=product_category_name,
        seller_id=seller_id,
        datatype=datatype,
        window_size=window_size,
    )

    response: HTTPResponseDTO = make_request_json(f'forecast', method='POST', body=body)

    if response['success']:
        body: ForecastResponseDTO = response['body']
        df = pd.DataFrame(body['result'])
        filters = body['filter']

        return response['success'], df, filters

    else:
        return response['success'], response.get('message', 'error making request'), None
