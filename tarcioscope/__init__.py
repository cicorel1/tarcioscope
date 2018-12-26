import os

from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from tarcioscope import api, config
    app.register_blueprint(api.bp)
    app.register_blueprint(config.bp)

    return app
