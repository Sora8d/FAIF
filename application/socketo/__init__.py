from flask import Blueprint

bp= Blueprint('socketo', __name__)

from application.socketo import so
