from flask import Blueprint

micropub_bp = Blueprint('micropub_bp', __name__)

from . import views
