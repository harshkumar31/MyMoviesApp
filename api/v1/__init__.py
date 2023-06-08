from sanic import Blueprint
from .routes import auth, lists, movie, searches

v1 = Blueprint.group(auth, lists, movie, searches, url_prefix="/v1")
