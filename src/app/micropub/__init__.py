from flask import Blueprint

micropub_bp = Blueprint("micropub_bp", __name__, template_folder="templates")

from . import views