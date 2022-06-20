from typing import List, Union
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    url_for,
)
from flask_login import login_required as _login_required, current_user
import functools

auth_bp = Blueprint("auth", __name__, template_folder="templates")


def login_required(verified_only=True):
    def layer(func):
        @_login_required
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if (
                not current_user.is_verified
                and current_app.config["ACCOUNT_VERIFICATION"]
                and verified_only
            ):
                return redirect(url_for("user.profile_not_verified"))
            return func(*args, **kwargs)

        return wrapper

    return layer


def verification_setting_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not current_app.config["ACCOUNT_VERIFICATION"]:
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)

    return wrapper


def role_required(role: Union[str, int, List[Union[str, int]]]):
    def layer(func):
        @login_required()
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            roles = [role] if not isinstance(role, list) else role

            if not current_user.role.name in roles and not current_user.role_id in roles:
                flash("Your user doesn't have permission", "danger")
                return redirect(url_for("core.home"))
            return func(*args, **kwargs)

        return wrapper

    return layer


from .routes import auth_bp
