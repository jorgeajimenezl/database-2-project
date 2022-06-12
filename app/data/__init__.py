from flask import Blueprint

data_bp = Blueprint("data", __name__, template_folder="templates")

from .routes import data_bp