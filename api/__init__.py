import requests_cache
from flask import Flask

from .models import db


def create_app(config="config.Config"):
    """Application factory"""
    app = Flask(__name__, instance_relative_config=True)

    requests_cache.install_cache('postcode_cache', backend='sqlite', expire_after=180)

    app.config.from_object(config)
    db.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()

    return app
