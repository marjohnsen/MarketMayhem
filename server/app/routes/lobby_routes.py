from flask import Blueprint, Response, request, jsonify
from app.models import Session, Player, SessionState
from typing import Dict, Any, Tuple
from app.db import db
import re

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
    session_key: str = data.get("session_key", "")
    player_name: str = data.get("player_name", "")

    if not session_key or not player_name:
        return jsonify({"error": "Missing session_key or player_name"}), 400

    if not re.match(r"^[a-zA-Z0-9]+$", player_name) or not (3 <= len(player_name) <= 20):
        return jsonify({"error": "Player name can only contain between 3 and 20 alphanumeric characters"}), 400

    # Load and validate the session
    session = Session.query.filter_by(key=session_key).first()

    if not session:
        return jsonify({"error": "Session not found"}), 400

    if session.state != SessionState.LOBBY:
        return jsonify({"error": "The game has started and the lobby is closed."}), 400

    # Load and validate the player
    if existing_player := Player.query.filter_by(name=player_name, session_id=session.id).first():
        return jsonify({"error": f"Player '{existing_player.name}' already exists"}), 400

    # Create and commit the player
    try:
        new_player = Player(name=player_name, session_id=session.id)
        db.session.add(new_player)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    # Return the success message and the player key
    return jsonify(
        {
            "message": f"Player {player_name} has successfully joined the session.",
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
