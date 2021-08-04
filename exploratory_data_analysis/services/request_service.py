
from typing import Dict, Literal
from constants.api_consts import API_URL
import requests
from dtos.http_response_dto import ResponseBodyDTO

HTTPMethods = Literal['GET', 'POST', 'PUT', 'DELETE']


def make_request_json(endpoint: str, body: Dict = None, method: HTTPMethods = 'GET') -> ResponseBodyDTO:
    url = f'{API_URL}/{endpoint}'

    if method == 'GET':
        response = requests.get(url)
    elif method == 'POST':
        response = requests.post(url, json=body)
    elif method == 'PUT':
        response = requests.put(url, json=body)
    elif method == 'DELETE':
        response = requests.delete(url)
    else:
        raise ValueError('method not exists')

    return response.json()
