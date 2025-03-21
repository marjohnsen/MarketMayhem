import re
from typing import Any, Dict, Tuple

from flask import Blueprint, Response, jsonify, request

from app.db import db
from app.models import Player, Session, SessionState
from app.validators import LobbyValidators

lobby_routes = Blueprint("lobby_routes", __name__)


@lobby_routes.route("/join_session", methods=["POST"])
def join_session() -> Tuple[Response, int]:
    """
    Allows a player to join a session using a session key.

    Request JSON must include:
    - 'session_key': The unique key of the session the player wants to join.
    - 'player_name': The name of the player joining.

    On success:
    - A new player is added to the session.

    Response:
    - A success message indicating success
    - The player's unique key
    """
    # Load and validate the request data
    data: Dict[str, Any] = request.get_json() or {}
    validators = LobbyValidators(data)
    (
        validators.require_fields(["session_key", "player_name"])
        .validate_session_key()
        .validate_player_name()
        .validate_state()
        .check_errors()
    )

    # Create and commit the player
    try:
        session = db.session.query(Session).filter_by(key=data["session_key"]).first()
        new_player = Player(name=data["player_name"], session_id=session.id)
        db.session.add(new_player)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    # Return the success message and the player key
    return jsonify(
        {
            "message": f"Player {data['player_name']} has successfully joined the session.",
            "player_key": new_player.key,
        }
    ), 200


@lobby_routes.route("/session_status", methods=["POST"])
def session_status() -> Tuple[Response, int]:
    """
    Returns the status of a session.
    Request JSON must include:
    - 'session_key': The unique key of the session to check.
    Response:
    - The status of the session.
    """
    # Load and validate the request data
    data: Dict[str, Any] = request.get_json() or {}
    session_key: str = data.get("session_key", "")
    player_key: str = data.get("player_key", "")

    if not session_key or not player_key:
        return jsonify({"error": "Missing session_key or player_key"}), 400

    if not session_key:
        return jsonify({"error": "Missing session_key"}), 400

    if not player_key:
        return jsonify({"error": "Missing player_key"}), 400

    # Load and validate the session
    session = Session.query.filter_by(key=session_key).first()
    if not session:
        return jsonify({"error": "Session not found"}), 400

    # Return the session status
    return jsonify({"status": session.state.value}), 200
