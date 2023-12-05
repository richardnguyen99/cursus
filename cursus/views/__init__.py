"""View module for the Cursus App
"""

import flask

from flask_login import current_user, login_required
from werkzeug.exceptions import BadRequest, NotFound

from .oauth import authorize, callback
from cursus.models import ActiveToken
from cursus.util import exceptions
from cursus.util.extensions import db, cache

SUPPORT_PUBLIC_ENDPOINTS = {
    "",
    "about",
    "demo",
    "docs",
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


@view_bp.after_request
def after(response: flask.Response):
    if "X-Response-SPA" in response.headers:
        return response

    response.add_etag()
    response.headers["Cache-Control"] = "public, max-age=0, must-revalidate"

    return response.make_conditional(flask.request)


@view_bp.route("/profile/revoke_token", methods=["GET"])
def profile_revoke():
    """Revoke an API token from the current user"""

    if not current_user.is_authenticated:
        return (
            flask.json.jsonify(
                {
                    "type": "error",
                    "message": "You must be logged in to revoke an API token",
                }
            ),
            401,
        )

    req = flask.request

    if req.method != "GET" and req.method != "HEAD":
        raise exceptions.MethodNotAllowedError(
            f"Method {req.method} not allowed for this endpoint"
        )

    old_token = ActiveToken.query.filter_by(user_id=current_user.id).first()

    if old_token:
        db.session.delete(old_token)
        db.session.commit()

        return (
            flask.json.jsonify(
                {"type": "success", "message": "Token revoked"}
            ),
            200,
        )

    return (
        flask.json.jsonify({"type": "info", "message": "No token found"}),
        200,
    )


@view_bp.route("/profile/generate_token", methods=["GET"])
def profile_generate():
    """Generate an API token for the current user"""

    if not current_user.is_authenticated:
        return (
            flask.json.jsonify(
                {"message": "You must be logged in to generate an API token"}
            ),
            401,
        )

    req = flask.request

    if req.method != "GET" and req.method != "HEAD":
        raise exceptions.MethodNotAllowedError(
            f"Method {req.method} not allowed for this endpoint"
        )

    token = ActiveToken(
        token=ActiveToken.generate_token(),
        user_id=current_user.id,
    )

    old_token = ActiveToken.query.filter_by(user_id=current_user.id).first()

    if old_token:
        db.session.delete(old_token)
        db.session.commit()

    # Commit the token to the database
    db.session.add(token)
    db.session.commit()

    return (
        flask.json.jsonify(
            {
                "id": current_user.id,
                "active_token": str(token),
                "revoked_token": str(old_token),
            }
        ),
        200,
    )


@view_bp.route("/profile", methods=["GET"])
@view_bp.route("/profile/", methods=["GET"])
@login_required
def profile():
    return flask.redirect(
        flask.url_for("views.profile_account", sub_page="account")
    )


@view_bp.route("/profile/<sub_page>")
def profile_account(sub_page: str):
    if not current_user.is_authenticated:
        return flask.redirect(flask.url_for("views.profile"))

    req = flask.request

    if req.method != "GET" and req.method != "HEAD":
        raise exceptions.MethodNotAllowedError(
            f"Method {req.method} not allowed for this endpoint"
        )

    content = flask.render_template(
        f"profile-{sub_page}.html",
        user_id=current_user.id,
        active_token=current_user.token,
    )

    if "X-Requested-SPA" in req.headers:
        resp = flask.make_response(content, 200)
        resp.headers["X-Response-SPA"] = "true"
    else:
        resp = flask.make_response(
            flask.render_template(
                "_profile.html",
                page_name="profile",
            )
        )

    return resp, 200


from . import public
