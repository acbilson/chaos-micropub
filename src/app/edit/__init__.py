from flask import Blueprint

edit_bp = Blueprint("edit_bp", __name__)

from . import views
