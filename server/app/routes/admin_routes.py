from typing import Any, Dict, Tuple, Union

from flask import Blueprint, Response, current_app, jsonify, request

from app.db import db
from app.models import Player, PlayerState, Session, SessionState
from app.validators.admin import AdminValidator
from game.engine import Exchange, SimulatorCatalog

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

    # Load and validate the request data
    data: Dict[str, Any] = request.get_json() or {}
    validator: AdminValidator = AdminValidator(data)
    validator.require_fields(["admin_key"]).validate_admin_key().check_errors()

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
    # Load and validate the request data
    data: Dict[str, Any] = request.get_json() or {}
    validator: AdminValidator = AdminValidator(data)

    (
        validator.require_fields(["admin_key", "session_key", "epochs"])
        .validate_admin_key()
        .validate_session_key()
        .validate_active_players()
        .validate_epochs()
        .check_errors()
    )

    # Create market simulator instance
    catalog = SimulatorCatalog()
    SimulatorClass = catalog["GaussianMarketSimulator"]
    market_simulator = SimulatorClass(epochs=10, volatility=0.1, decay=0.01)

    # Create exchange instance
    exchange = Exchange(market_simulator, 10)

    # Populate the exchange with active players
    players = db.session.query(Player).filter_by(session_id=data["session_key"], state=PlayerState.CONNECTED).all()
    for player in players:
        exchange.add_player(player.key)

    # Upload exchange to the current_app
    current_app.config["EXCHANGE"] = exchange

    # Update sesson and commit
    try:
        db.session.query(Session).filter_by(key=data["session_key"]).update({"state": SessionState.PLAYING})
        db.session.commit()
        return jsonify({"message": "The game has started"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


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
    validator: AdminValidator = AdminValidator(data)

    (
        validator.require_fields(["admin_key", "session_key", "player_name"])
        .validate_admin_key()
        .validate_session_key()
        .validate_player_key()
        .validate_new_state()
        .check_errors()
    )

    session_key = data["session_key"]
    player_name = data["player_name"]
    new_state = data["new_state"]

    # Change and commit the player state
    try:
        player = db.session.query(Player).filter_by(name=player_name, session_key=session_key).first()
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
