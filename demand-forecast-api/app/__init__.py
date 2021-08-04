from typing import Optional

from flask import Flask
from flask_cors import CORS

from app.config import DefaultConfig, envirioments_config


def create_app(environment: Optional[str] = None):
    from app.services import main_routes

    app = Flask(__name__)

    environment = environment.upper() if environment else 'DEV'

    config: DefaultConfig = envirioments_config.get(environment.upper())

    if config:
        app.config.from_object(config)
        config.init(app)

        app.register_blueprint(main_routes)

        CORS(app)
        return app
    else:
        raise ValueError('environment config not exists. Try DEV or PRODUCTION')
