from flask import Blueprint

quip_bp = Blueprint("quip_bp", __name__, template_folder="templates")

from . import views
