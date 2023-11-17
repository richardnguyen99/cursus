# -*- coding: utf-8 -*-

"""Cursus OAuth module with OAuth2 support
"""

import cuid2
import json
import flask
import secrets
import flask_login
import requests

from urllib.parse import urlencode

from cursus.models import Account, User
from cursus.util.extensions import db
from cursus.util.profile import get_profile
from cursus.util.account import get_account


def authorize(provider: str):
    if not flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for("views.show", page_name="index"))

    provider_data = flask.current_app.config["OAUTH2_PROVIDERS"].get(provider)
    if not provider_data:
        return flask.abort(404)

    flask.session["oauth2_state"] = secrets.token_urlsafe(16)

    query_string = urlencode(
        {
            "client_id": provider_data["client_id"],
            "redirect_uri": flask.url_for(
                "oauth.callback", provider=provider, _external=True
            ),
            "scope": " ".join(provider_data["scope"]),
            "response_type": "code",
            "state": flask.session["oauth2_state"],
            "access_type": provider_data.get("access_type", "online"),
        }
    )

    return flask.redirect(f"{provider_data['authorize_url']}?{query_string}")


def callback(provider: str):
    if not flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for("views.show", page_name="index"))

    provider_data = flask.current_app.config["OAUTH2_PROVIDERS"].get(provider)
    if not provider_data:
        return flask.abort(404)

    if flask.request.args.get("state") != flask.session["oauth2_state"]:
        return flask.abort(401)

    if "code" not in flask.request.args:
        return flask.abort(401)

    response = requests.post(
        provider_data["token_url"],
        data={
            "client_id": provider_data["client_id"],
            "client_secret": provider_data["client_secret"],
            "code": flask.request.args.get("code"),
            "redirect_uri": flask.url_for(
                "oauth.callback", provider=provider, _external=True
            ),
            "grant_type": "authorization_code",
        },
        headers={"Accept": "application/json"},
    )

    if response.status_code != 200:
        return flask.abort(401)

    oauth2_token = response.json().get("access_token")
    if not oauth2_token:
        return flask.abort(401)

    token_response = response.json()

    print(json.dumps(token_response, indent=4))

    response = requests.get(
        provider_data["userinfo"]["url"],
        headers={
            "Authorization": f"Bearer {oauth2_token}",
            "Accept": "application/json",
        },
    )

    if response.status_code != 200:
        return flask.abort(401)

    data_response = response.json()

    uniform_account = get_account(provider, token_response, data_response)
    account_from_database = (
        db.session.query(Account)
        .filter_by(
            provider=uniform_account.provider,
            providerAccountId=uniform_account.providerAccountId,
        )
        .first()
    )

    # Account has not registered with this app
    if account_from_database is None:
        profile = get_profile(provider, data_response)
        profile.id = cuid2.Cuid(length=11).generate()
        uniform_account.userId = profile.id

        db.session.add(profile)
        db.session.add(uniform_account)

    else:
        account_from_database.refresh_token = uniform_account.refresh_token

    db.session.commit()

    print(json.dumps(data_response, indent=4))

    return flask.redirect(flask.url_for("views.show", page_name="index"))
