from flask import render_template

from .forms import TruckForm
from ..auth import login_required
from . import data_bp


@data_bp.route("/register_truck")
def register_truck():
    form = TruckForm()
    return render_template("data/register_truck.html", form=form)
