from flask import Blueprint

note_bp = Blueprint("note_bp", __name__, template_folder="templates")

from . import views
