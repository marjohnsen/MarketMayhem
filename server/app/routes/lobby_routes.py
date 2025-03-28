from typing import Any, Dict, Tuple, cast
from flask import Blueprint, Response, jsonify, request

from app.db import db
from app.models import Player, Session
from app.validators import LobbyValidators

lobby_routes = Blueprint("lobby_routes", __name__)


@lobby_routes.route("/join_session", methods=["POST"])
def join_session() -> Tuple[Response, int]:
    """
    Allows a player to join a session using a session key.
    """
    data: Dict[str, Any] = request.get_json() or {}
    validators = LobbyValidators(data)

    (
        validators.require_fields(["session_key", "player_name"])
        .validate_session_key()
        .validate_new_player_name()
        .validate_state()
        .check_errors()
    )

    new_player = Player(name=data["player_name"], session_key=data["session_key"])  # type: ignore
    db.session.add(new_player)
    db.session.commit()

    return jsonify(
        {"message": f"Player {data['player_name']} has successfully joined the session.", "player_key": new_player.key}
    ), 200


@lobby_routes.route("/get_session_status", methods=["POST"])
def get_session_status() -> Tuple[Response, int]:
    """
    Returns the status of a session.
    """
    data: Dict[str, Any] = request.get_json() or {}
    session_key: str = data.get("session_key", "")

    validators = LobbyValidators(data)

    (
        validators.require_fields(["session_key", "player_key"])
        .validate_player_key()
        .validate_session_key()
        .check_errors()
    )

    session = cast(Session, Session.query.filter_by(key=session_key).first())
    return jsonify({"status": session.state.value}), 200
