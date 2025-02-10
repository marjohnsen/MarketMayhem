from flask import Blueprint
from app.routes.admin_routes import admin_routes
from app.routes.lobby_routes import lobby_routes
from app.routes.game_routes import game_routes

routes = Blueprint("routes", __name__)

routes.register_blueprint(admin_routes)
routes.register_blueprint(lobby_routes)
routes.register_blueprint(game_routes)
