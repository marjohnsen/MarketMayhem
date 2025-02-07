from flask import Blueprint
from app.routes.lobby_routes import lobby_routes

routes = Blueprint("routes", __name__)

routes.register_blueprint(lobby_routes)
