import flask
from app.controllers import forecast_controller
from app.dtos.forecast_dtos import ForecastRequestDTO
from app.utils.http_utils import make_http_response

from . import main_routes


@main_routes.route('/forecast', methods=['POST'])
def forecast():

    body : ForecastRequestDTO = flask.request.get_json()
    
    response = forecast_controller.make_forecast(body)

    return make_http_response(response)
