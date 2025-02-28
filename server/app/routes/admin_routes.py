from flask import Blueprint, Response, request, jsonify, current_app
from app.models import Session, Player, PlayerState
from typing import Dict, Any, Tuple, Union
from app.db import db
from game import engine

admin_routes = Blueprint("admin_routes", __name__)


@admin_routes.route("/create_session", methods=["POST"])
def create_session() -> Tuple[Response, int]:
    """
    Creates a new session for a game.

    Request JSON must include:
    - 'admin_key': the admin password to authorize session creation.

    Validations:
    - Ensures the 'admin_key' is provided and matches the admin password.

    On success:
    - A new session is created and added to the database.

    Response:
    - A success message indicating the session was created.
    - The session key players can use to join the session.
    """

    # Load the request data
    data: Dict[str, Any] = request.get_json() or {}
    admin_key: str = data.get("admin_key", "")

    # Check authorization
    if admin_key != current_app.config["ADMIN_KEY"]:
        return jsonify({"error": f"{admin_key}, {current_app.config["ADMIN_KEY"]}"}), 401

    # Create and commit new session
    try:
        session: Session = Session()
        db.session.add(session)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    # Return the session key
    response_data: Dict[str, str] = {
        "message": "Session created. Share this key with players to join the session.",
        "session_key": session.key,
    }
    return jsonify(response_data), 201


@admin_routes.route("/start_game", methods=["POST"])
def start_game() -> Tuple[Response, int]:
    """
    Starts the game.
    """
    # Load the request data
    data: Dict[str, Any] = request.get_json() or {}
    admin_key: str = data.get("admin_key", "")
    session_key: str = data.get("session_key", "")

    # Check authorization
    if admin_key != current_app.config["ADMIN_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401

    # Load and validate the session
    if not (session := db.session.query(Session).filter_by(key=session_key).first()):
        return jsonify({"error": f"Session with key '{session_key}' not found"}), 400

    # Check if there are enough players to start the game
    if not any(player.state == PlayerState.CONNECTED for player in session.players):
        return jsonify({"error": "Cannot start the with no players."}), 400

    # Add game instance to the session

    

     try:
         db.session.commit()
     except Exception as e:
         db.session.rollback()
   #     return jsonify({"error": str(e)}), 500

    return jsonify({"message": "good!"}), 200


@admin_routes.route("/change_player_state", methods=["POST"])
def change_player_state() -> Tuple[Response, int]:
    """
    Change player state.

    Request JSON must include:
    - 'admin_key': the admin password to authorize the action.
    - 'session_key': the key of the session the player is in.
    - 'player_name': the name of the player whose state is being changed.
    - 'new_state': the new state to assign to the player.

    Validations:
    - Ensures 'admin_key' matches the stored admin password.
    - Ensures 'session_key' corresponds to an existing session.
    - Ensures 'player_name' corresponds to a player in the specified session.
    - Ensures 'new_state' is a valid PlayerState value.

    On success:
    - The player's state is updated.

    Response:
    - A success message confirming the player's state change.
    """

    # Load the request data
    data: Dict[str, Any] = request.get_json() or {}
    admin_key: str = data.get("admin_key", "")
    session_key: str = data.get("session_key", "")
    player_name: str = data.get("player_name", "")
    new_state: Union[str, PlayerState] = data.get("new_state", "")

    # Check authorization
    if admin_key != current_app.config["ADMIN_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401

    # Load and validate the session
    if not (session := db.session.query(Session).filter_by(key=session_key).first()):
        return jsonify({"error": f"Session with key '{session_key}' not found"}), 400

    # Load and validate the player
    if not (player := db.session.query(Player).filter_by(name=player_name, session_id=session.id).first()):
        return jsonify({"error": f"Player '{player_name}' not found in session '{session_key}'"}), 400

    # Validate new state
    valid_states = {state.value for state in PlayerState}
    if new_state not in valid_states:
        return jsonify({"error": f"Invalid state '{new_state}'. Must be one of {list(valid_states)}"}), 400

    # Change and commit the player state
    try:
        old_state = player.state
        new_state = PlayerState(new_state)
        player.state = new_state
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    # Return success message
    return jsonify(
        {
            "message": f"Player '{player_name}' state changed from {old_state} to '{new_state}' in session '{session_key}'"
        }
    ), 200
