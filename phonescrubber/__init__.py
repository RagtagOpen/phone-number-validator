from flask import Flask
from phonescrubber.config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from phonescrubber.numbers import numbers_bp
    app.register_blueprint(numbers_bp)

    return app
