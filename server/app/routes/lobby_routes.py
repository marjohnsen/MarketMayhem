from flask import Blueprint, request, jsonify, current_app
from app.models import db, Game, Player
import re

lobby_routes = Blueprint("lobby_routes", __name__)


@lobby_routes.route("/new_game", methods=["POST"])
def create_game():
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

    # Load and validate the request data
    data = request.get_json()
    admin_key = data.get("admin_key")
    if admin_key != current_app.config["ADMIN_KEY"]:
        return jsonify({"error": "Unauthorized"}), 401

    # Create a new game
    game = Game()
    db.session.add(game)
    db.session.commit()

    # Return the game key
    return jsonify(
        {
            "message": "Game created. Share this key with players to join the lobby.",
            "game_key": game.key,
        }
    ), 201


@lobby_routes.route("/join_game", methods=["POST"])
def join_game():
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
    data = request.get_json()
    game_key = data.get("game_key")
    player_name = data.get("player_name")

    if not game_key or not player_name:
        return jsonify({"error": "Missing game_key or player_name"}), 400

    if not re.match(r"^[a-zA-Z0-9]+$", player_name) or not (3 <= len(player_name) <= 20):
        return jsonify({"error": "Player name can only contain between 3 and 20 alphanumeric characters"}), 400

    # Load and validate the game
    game = Game.query.filter_by(key=game_key).first()

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
