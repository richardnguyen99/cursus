# -*- coding: utf-8 -*-
"""Flask Management Script"""

import os
import click
import waitress

from werkzeug.middleware.proxy_fix import ProxyFix
from flask.cli import FlaskGroup, with_appcontext
from dotenv import load_dotenv

from cursus import create_app
from cursus.util.extensions import db, assets


# Not being accessed directly. However, it is required for the migrations to
# know where to find the models.
from cursus.models import (  # noqa: F401 # pylint: disable=unused-import
    university,
    country,
    user,
    token,
    history,
    course,
    department,
)


# Initialize the core management script
@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Management script for the Flask application."""


@cli.command("create-db")
@with_appcontext
def create_db():
    """Create the database."""

    db.create_all()
    db.session.commit()


@cli.command("waitress")
@click.option("--host", default="0.0.0.0", help="Host IP to bind to")
@click.option("--port", default=8000, help="Port to bind to")
def run_waitress(host, port):
    """Run the application using Waitress as the production server."""

    # Load the environment variables from the .env file manually as `waitress`
    # does not include the environment variables loading by default like Flask.
    load_dotenv()

    # Assert some environment variables are set
    assert os.environ.get("DATABASE_URL")
    assert os.environ.get("FLASK_ENV")

    # https://stackoverflow.com/questions/11981187/flask-assets-and-flask-testing-throws-registererror-another-bundle-is-already-r
    assets._named_bundles = {}  # pylint: disable=protected-access

    app = create_app()
    app = ProxyFix(app, x_for=1, x_host=1)
    print(f"Running waitress on {host}:{port}")

    waitress.serve(app, host=host, port=port)


if __name__ == "__main__":
    cli()
