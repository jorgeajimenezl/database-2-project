from ..auth import login_required
from . import data_bp


@data_bp.route("/manage")
@login_required
def manage_dashboard():
    return "Tampoco mires aquí"
