from flask import Blueprint

numbers_bp = Blueprint('numbers', __name__)

from . import views
