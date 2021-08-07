from app.dtos.http_response_dto import HTTPResponseDTO
import flask
from app.controllers import forecast_controller
from app.dtos.forecast_dtos import ForecastRequestDTO
from app.utils.http_utils import make_http_response

from . import main_routes


@main_routes.route('/forecast', methods=['POST'])
def forecast():

    body : ForecastRequestDTO = flask.request.get_json()
    
    result = forecast_controller.make_forecast(body)

    success = True if result is not None else False
    msg = '' if success else 'Erro while process data'

    response = HTTPResponseDTO(body=result, success=success, message=msg)

    return make_http_response(response)
