from flask import redirect, render_template, url_for

from . import core_bp
from ..auth import login_required


@core_bp.route("/")
@core_bp.route("/home")
@login_required()
def home():
    return render_template("core/home.html")
    # return redirect(url_for("user.profile"))
