from app.dtos.http_response_dto import HTTPResponseDTO
import flask


def make_http_response(body: HTTPResponseDTO, code: int = None):

    if code is None and body.get('code') is None:
        code = 200 if body.get('success') else 400
        body['code'] = code

    return flask.make_response(body, body['code'])
