"""View module for the Cursus App
"""

import flask

from flask_login import current_user, login_required
from werkzeug.exceptions import BadRequest, NotFound

from cursus.util import exceptions
from .oauth import authorize, callback

SUPPORT_PUBLIC_ENDPOINTS = {
    "",
    "about",
    "demo",
    "docs",
}

SUPPORT_DOCS_ENDPOINTS = {
    "search.html",
    "details.html",
    "courses.html",
    "campus.html",
    "domains.html",
    "more.html",
}

view_bp = flask.Blueprint(
    "views",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)

oauth_bp = flask.Blueprint("oauth", __name__, url_prefix="/oauth")

oauth_bp.add_url_rule(
    "/authorize/<provider>",
    view_func=authorize,
    methods=["GET"],
)

oauth_bp.add_url_rule(
    "/callback/<provider>",
    view_func=callback,
    methods=["GET"],
)


@view_bp.app_errorhandler(exceptions.BadRequestError)
@view_bp.app_errorhandler(BadRequest)
@view_bp.app_errorhandler(400)
def handle_bad_request(error):
    req = flask.request
    msg = f"Bad Request: {req.method} {req.url}"

    if isinstance(error, BadRequest):
        msg = error.get_description()
    elif isinstance(error, exceptions.BadRequestError):
        msg = error.get_reason()

    return flask.render_template("400.html", msg=msg), 400


@view_bp.app_errorhandler(exceptions.NotFoundError)
@view_bp.app_errorhandler(NotFound)
@view_bp.app_errorhandler(404)
def handle_not_found(error):
    req = flask.request
    msg = f"Not found: {req.url}"

    if isinstance(error, NotFound):
        msg = error.get_description()
    elif isinstance(error, exceptions.NotFoundError):
        msg = error.get_reason()

    return (
        flask.render_template(
            "4xx.html",
            title="Not found",
            status_message="Not found",
            status_code=404,
            reason=msg,
        ),
        404,
    )


@view_bp.route("/login", methods=["GET"])
def login():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("views.show", page_name="index"))

    req = flask.request

    if req.method != "GET":
        raise exceptions.MethodNotAllowedError(
            f"Method {req.method} not allowed for this endpoint"
        )

    next = req.args.get("next")

    return flask.render_template("login.html", next=next), 200


@view_bp.route("/", defaults={"page_name": "index"}, methods=["GET"])
@view_bp.route("/<page_name>", methods=["GET"])
def show(page_name):
    req = flask.request

    url = req.path
    endpoint = url.split("/")[1]

    if endpoint not in SUPPORT_PUBLIC_ENDPOINTS:
        raise exceptions.NotFoundError(f"Page {page_name} not found")

    if req.method != "GET":
        raise exceptions.MethodNotAllowedError(
            f"Method {req.method} not allowed for this endpoint"
        )

    resp = flask.render_template(f"{page_name}.html", page_name=page_name)

    return resp, 200


@view_bp.route("/docs/<page_name>", methods=["GET"])
def docs(page_name: str):
    req = flask.request

    if page_name not in SUPPORT_DOCS_ENDPOINTS:
        raise exceptions.NotFoundError(f"Page {page_name} not found")

    if req.method != "GET":
        raise exceptions.MethodNotAllowedError(
            f"Method {req.method} not allowed for this `/docs/` endpoint"
        )

    resp = flask.render_template(f"doc-{page_name}", page_name="docs")

    return resp, 200


@view_bp.route("/profile", methods=["GET"])
@login_required
def profile():
    if not current_user.is_authenticated:
        return flask.redirect(flask.url_for("views.login"))

    req = flask.request

    if req.method != "GET":
        raise exceptions.MethodNotAllowedError(
            f"Method {req.method} not allowed for this endpoint"
        )

    return flask.render_template("profile.html"), 200
