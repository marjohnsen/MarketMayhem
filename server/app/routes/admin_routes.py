from typing import Any, Dict, Tuple, cast

from flask import Blueprint, Response, current_app, jsonify, request

from app.db import db
from app.game import games
from app.models import Player, PlayerState, Session, SessionState
from app.validators import AdminValidators
from game.engine import GameEngine

admin_routes = Blueprint("admin_routes", __name__)


@admin_routes.route("/create_session", methods=["POST"])
def create_session() -> Tuple[Response, int]:
    data: Dict[str, Any] = request.get_json() or {}
    validators = AdminValidators(data)
    validators.require_fields(["admin_key"]).validate_admin_key().check_errors()

    session: Session = Session()
    db.session.add(session)
    db.session.commit()

    response_data: Dict[str, str] = {
        "message": "Session created. Share this key with players to join the session.",
        "session_key": session.key,
    }
    return jsonify(response_data), 201


@admin_routes.route("/start_game", methods=["POST"])
def start_game() -> Tuple[Response, int]:
    data: Dict[str, Any] = request.get_json() or {}
    validators = AdminValidators(data)

    (
        validators.require_fields(["admin_key", "session_key", "epochs", "timestep"])
        .validate_admin_key()
        .validate_session_key()
        .validate_active_players()
        .validate_epochs()
        .validate_timestep()
        .check_errors()
    )

    players = (
        db.session.query(Player)
        .filter_by(session_key=data["session_key"], state=PlayerState.CONNECTED)
        .all()
    )
    player_keys = [player.key for player in players]
    games[data["session_key"]] = GameEngine(
        player_keys, data["epochs"], data["timestep"]
    )
    games[data["session_key"]].start()

    db.session.query(Session).filter_by(key=data["session_key"]).update(
        {"state": SessionState.PLAYING}
    )
    db.session.commit()

    return jsonify({"message": "The game has started"}), 200


@admin_routes.route("/change_player_state", methods=["POST"])
def change_player_state() -> Tuple[Response, int]:
    data: Dict[str, Any] = request.get_json() or {}
    validators = AdminValidators(data)

    (
        validators.require_fields(["admin_key", "session_key", "player_name"])
        .validate_admin_key()
        .validate_session_key()
        .validate_player_name()
        .validate_new_state()
        .check_errors()
    )

    session_key = data["session_key"]
    player_name = data["player_name"]
    new_state = data["new_state"]

    player = cast(
        Player,
        db.session.query(Player)
        .filter_by(name=player_name, session_key=session_key)
        .first(),
    )
    old_state = player.state
    new_state = PlayerState(new_state)
    player.state = new_state
    db.session.commit()

    return jsonify(
        {
            "message": f"Player '{player_name}' state changed from {old_state} to '{new_state}' in session '{session_key}'"
        }
    ), 200
