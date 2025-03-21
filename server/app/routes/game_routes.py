from flask import Blueprint, request, jsonify, current_app
from app.db import db
from typing import Any, Dict, Tuple

game_routes = Blueprint("game_routes", __name__)


@game_routes.route("/get_latest_price", methods=["POST"])
def get_latest_price():
    data: Dict[str, Any] = request.get_json() or {}

    epoch, latest_price = current_app.config["game"].exchange.get_latest_price()

    response: Dict[str, str] = {"epoch": epoch, "latest_price": latest_price}
    return jsonify(response), 201
