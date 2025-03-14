from flask import Blueprint, request, jsonify, current_app
from app.db import db
from typing import Any, Dict, Tuple

game_routes = Blueprint("game_routes", __name__)


@game_routes.route("/fetch_latest_price", methods=["POST"])
def fetch_latest_price():
    data: Dict[str, Any] = request.get_json() or {}

    return jsonify(data), 201

latest_price current_app.config["game"].exchange.market.log_return
