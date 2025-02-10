from flask import Blueprint, Response, request, jsonify
from app.models import db, Game, Player
from typing import Dict, Any, Tuple
import re

lobby_routes = Blueprint("lobby_routes", __name__)


@lobby_routes.route("/join_game", methods=["POST"])
def join_game() -> Tuple[Response, int]:
    """
    Allows a player to join a game using a game key.

    Request JSON must include:
    - 'game_key': The unique key of the game the player wants to join.
    - 'player_name': The name of the player joining.

    Validations:
    - Ensures both 'game_key' and 'player_name' are provided.
    - Checks if the player name is at most 20 characters long.
    - Ensures the player name contains only alphanumeric characters (A-Z, a-z, 0-9).
    - Checks if the game exists based on the provided key.
    - Ensures the game is still in the 'lobby' state (i.e., hasn't started yet).
    - Prevents duplicate player names within the same game.

    On success:
    - A new player is added to the game.

    Response:
    - A success message indicating success
    - The player's unique key
    """
    # Load and validate the request data
    data: Dict[str, Any] = request.get_json() or {}
    game_key: str = data.get("game_key", "")
    player_name: str = data.get("player_name", "")

    if not game_key or not player_name:
        return jsonify({"error": "Missing game_key or player_name"}), 400

    if not re.match(r"^[a-zA-Z0-9]+$", player_name) or not (3 <= len(player_name) <= 20):
        return jsonify({"error": "Player name can only contain between 3 and 20 alphanumeric characters"}), 400

    # Load and validate the game
    game: Game = Game.query.filter_by(key=game_key).first()

    if not game:
        return jsonify({"error": "Game not found"}), 400

    if game.state != "lobby":
        return jsonify({"error": "Game has already started"}), 400

    # Load and validate the player
    if existing_player := Player.query.filter_by(name=player_name, game_id=game.id).first():
        return jsonify({"error": f"Player '{existing_player.name}' already exists"}), 400

    new_player = Player(name=player_name, game_id=game.id)
    db.session.add(new_player)
    db.session.commit()

    # Return the player key
    return jsonify(
        {
            "message": f"Player {player_name} has successfully joined the game.",
            "player_key": new_player.key,
        }
    ), 200
