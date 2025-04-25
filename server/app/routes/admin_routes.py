from typing import Any, Dict, Tuple

from flask import Blueprint, Response, jsonify, make_response, request

from app.db import db
from app.game import games
from app.models import Lobby, Player
from app.validators import AdminValidators
from game.engine import GameEngine

admin_routes = Blueprint("admin_routes", __name__)


@admin_routes.route("/create_game", methods=["POST"])
def create_game() -> Tuple[Response, int]:
    data: Dict[str, Any] = request.get_json() or {}
    validators = AdminValidators(data)

    (
        validators.require_fields(["admin_key", "epochs", "timestep"])
        .validate_admin_key()
        .validate_epochs()
        .validate_timestep()
        .check_errors()
    )

    lobby: Lobby = Lobby()
    db.session.add(lobby)
    db.session.commit()

    games[lobby.key] = GameEngine(data["epochs"], data["timestep"])

    response_data: Dict[str, str] = {
        "game_key": lobby.key,
    }
    return make_response(jsonify(response_data), 201)


@admin_routes.route("/start_game", methods=["POST"])
def start_game() -> Tuple[Response, int]:
    data: Dict[str, Any] = request.get_json() or {}
    validators = AdminValidators(data)

    (
        validators.require_fields(["admin_key", "game_key"])
        .validate_admin_key()
        .validate_game_key()
        .validate_active_players()
        .check_errors()
    )

    players = db.session.query(Player).filter_by(game_key=data["game_key"]).all()
    player_keys = [player.key for player in players]
    games[data["game_key"]].start(player_keys)

    return jsonify({"message": "The game has started"})


@admin_routes.route("/stop_game", methods=["POST"])
def stop_game() -> Tuple[Response, int]:
    data: Dict[str, Any] = request.get_json() or {}
    validators = AdminValidators(data)

    (
        validators.require_fields(["admin_key", "game_key"])
        .validate_admin_key()
        .validate_game_key()
        .check_errors()
    )

    games[data["game_key"]].stop()

    return jsonify({"message": "The game has stopped"})
