from flask import Blueprint

bp = Blueprint('main', __name__)
import application.main.routes
