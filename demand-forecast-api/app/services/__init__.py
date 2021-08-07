
from flask import Blueprint

main_routes = Blueprint('api', __name__, url_prefix='/api')

from . import report_service, model_service # isort:skip
