from flask import Blueprint, Response, request, jsonify, current_app
from app.models import db, Game, Player, PlayerState
from typing import Dict, Any, Tuple

admin_routes = Blueprint("admin_routes", __name__)


@admin_routes.route("/new_game", methods=["POST"])
def create_game() -> Tuple[Response, int]:
    """
    Creates a new game and returns the game key.

    Request JSON must include:
    - 'password': the admin password to authorize game creation.

    Validations:
    - Ensures the 'admin_key' is provided and matches the admin password.

    On success:
    - A new game is created and added to the database.

    Response:
    - A success message indicating the game was created.
    - The game key that players can use to join the game.
    """

    # Load and the request data
    data: Dict[str, Any] = request.get_json() or {}
    admin_key: str = data.get("admin_key", "")

    # Check authorization
    if admin_key != current_app.config["ADMIN_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401

    # Create a new game
    game: Game = Game()
    db.session.add(game)

    # Commit the changes
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    # Return the game key
    response_data: Dict[str, str] = {
        "message": "Game created. Share this key with players to join the lobby.",
        "game_key": game.key,
    }
    return jsonify(response_data), 201


@admin_routes.route("/kick_player", methods=["POST"])
def ban_player() -> Tuple[Response, int]:
    # Load and validate the request data
    data: Dict[str, Any] = request.get_json() or {}
    admin_key: str = data.get("admin_key", "")
    game_key: str = data.get("game_key", "")
    player_name: str = data.get("player_name", "")

    # Check authorization
    if admin_key != current_app.config["ADMIN_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401

    # Load the game
    if not (game := db.session.query(Game).filter_by(key=game_key).first()):
        return jsonify({"error": f"Game with key '{game_key}' not found"}), 400

    # Load the player
    if not (player := db.session.query(Player).filter_by(name=player_name, game_id=game.id).first()):
        return jsonify({"error": f"Player '{player_name}' not found"}), 400

    # Change the player state
    player.state = PlayerState.BANNED

    # Commit the changes
    try:
        db.session.commit()
        return jsonify({"message": f"Player '{player_name}' has been banned from game '{game_key}'"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
