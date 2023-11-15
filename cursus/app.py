# -*- coding: utf-8 -*-

"""Cursus app factory module
"""

import os
import flask

from flask import Flask
from logging.config import dictConfig

from .apis import find_bp, university_bp as university_bp_v1
from .views import view_bp, oauth_bp
from .util.extensions import db, migrate, ma, login_manager


if os.environ.get("FLASK_ENV") != "development":
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s >>> %(message)s",
                    "datefmt": "%Y-%m-%dT%H:%M:%SZ",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
                "size-rotate": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": "cursus.log",
                    "maxBytes": 1024 * 1024 * 5,
                    "backupCount": 5,
                    "formatter": "default",
                },
            },
            "root": {
                "level": "INFO",
                "handlers": ["console", "size-rotate"],
            },
        }
    )


def create_app() -> Flask:
    """App factory function to create a Flask app instance

    The pattern is carefully described in the Flask documentation

    :see https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/
    """

    # Create a Flask application
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration for the application
    app.config.from_object(os.environ.get("APP_SETTINGS"))

    # Register Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    login_manager.init_app(app)

    # Register views
    app.register_blueprint(find_bp)
    app.register_blueprint(university_bp_v1)
    app.register_blueprint(view_bp)
    app.register_blueprint(oauth_bp)

    @login_manager.user_loader
    def load_user(id):
        return "user-id"

    @app.route("/ping")
    def ping():
        resp = flask.make_response(flask.json.dumps({"message": "pong"}), 200)
        resp.headers["Content-Type"] = "application/json"

        return resp

    @app.route("/")
    def hello():
        resp = flask.make_response(
            flask.json.dumps({"message": "Welcome to the Cursus API"}), 200
        )
        resp.headers["Content-Type"] = "application/json"

        return resp

    @app.route("/config")
    def config():
        return flask.jsonify({"message": app.config["DATABASE_URL"]})

    @app.after_request
    def after(response: flask.Response):
        current_app = flask.current_app
        req = flask.request

        current_app.logger.info(
            f'"{req.remote_addr}" {req.method} {req.path} \
{response.status_code} {response.content_length}'
        )

        return response

    @app.teardown_appcontext
    def shutdown_session(exception=None):  # pylint: disable=unused-argument
        db.session.remove()

    return app
