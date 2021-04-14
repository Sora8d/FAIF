from flask import Blueprint

bp = Blueprint('messages', __name__)

from application.messages import routes
