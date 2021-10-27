from flask import Blueprint

log_bp = Blueprint("log_bp", __name__, template_folder="templates")

from . import views
