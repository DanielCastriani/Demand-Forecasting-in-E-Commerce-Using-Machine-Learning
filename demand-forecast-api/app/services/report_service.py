from app.dtos.report_dtos import RequestReportDTO
import flask
from app.utils.http_utils import make_http_response
from app.controllers import report_controller

from . import main_routes


@main_routes.route('/report_list', methods=['GET'])
def report_list():
    response = report_controller.get_report_list()

    return make_http_response(response)


@main_routes.route('/report', methods=['POST'])
def report():

    body : RequestReportDTO = flask.request.get_json()
    
    response = report_controller.get_report_data(body)

    return make_http_response(response)

@main_routes.route('/performance_report', methods=['GET'])
def report_performace():
    
    response = report_controller.get_model_performance_report()

    return make_http_response(response)
