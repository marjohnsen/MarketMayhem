import re
from typing import Any, Dict, List, Self

from flask import abort, current_app, jsonify

from app.db import db
from app.game import games
from app.models import Player, Lobby


class BaseValidators:
    """Base class for route-specific validators."""

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize the validator with the request data."""
        self.data: Dict[str, Any] = data
        self.errors: List[str] = []

    def check_errors(self) -> Self:
        """Return all collected errors if any exist."""
        if self.errors:
            response = jsonify({"error": "Validation failed", "details": self.errors})
            response.status_code = 400
            abort(response)
        return self

    def require_fields(self, required_fields: list) -> Self:
        """Ensure all required fields are present and not empty."""
        missing = [field for field in required_fields if not self.data.get(field)]
        if missing:
            response = jsonify({"Missing fields": f"{', '.join(missing)}"})
            response.status_code = 400
            abort(response)
        return self

    def validate_admin_key(self) -> Self:
        """Check if the admin key is valid."""
        if self.data.get("admin_key") != current_app.config["ADMIN_KEY"]:
            self.errors.append("Invalid admin key.")
        return self

    def validate_game_key(self) -> Self:
        """Ensure the session exists."""
        game_key = self.data.get("game_key")
        if not db.session.query(Lobby).filter_by(key=game_key).first():
            self.errors.append(f"Game '{game_key}' not found.")
        return self

    def validate_player_key(self) -> Self:
        """Ensure the player exists in the session."""
        player_key = self.data.get("player_key")
        game_key = self.data.get("game_key")
        if not db.session.query(Player).filter_by(key=player_key, game_key=game_key).first():
            self.errors.append(f"Player '{player_key}' not found in session '{game_key}'.")
        return self

    def validate_player_name(self) -> Self:
        """Ensure the player exists in the session."""
        player_name = self.data.get("player_name")
        game_key = self.data.get("game_key")
        if not db.session.query(Player).filter_by(name=player_name, game_key=game_key).first():
            self.errors.append(f"Player '{player_name}' not found in session '{game_key}'.")
        return self


class AdminValidators(BaseValidators):
    def validate_epochs(self) -> Self:
        """Ensure epochs is an int and within the required range."""
        epochs = self.data.get("epochs")

        if not isinstance(epochs, int):
            self.errors.append("Epochs must be an integer")
            return self

        if not (60 <= epochs <= 600):
            self.errors.append("Epochs must be an integer between 60 and 600")
        return self

    def validate_timestep(self) -> Self:
        """Ensure timestep is an int and within the required range."""
        timestep = self.data.get("timestep")

        if not isinstance(timestep, int):
            self.errors.append("Timestep must be an integer")
            return self

        if not (1 <= timestep <= 10):
            self.errors.append("Timestep must be an integer between 1 and 10")
        return self

    def validate_active_players(self) -> Self:
        """Ensure there are active players in the session."""
        game_key = self.data.get("game_key")

        players = db.session.query(Player).filter_by(game_key=game_key).count()

        if players == 0:
            self.errors.append("Cannot start the game with no players.")

        return self


class GameValidators(BaseValidators):
    def validate_new_player_name(self) -> Self:
        """Ensure the player name is valid."""
        player_name = str(self.data.get("player_name"))
        game_key = self.data.get("game_key")

        if not re.match(r"^[a-zA-Z0-9]+$", player_name) or not (3 <= len(player_name) <= 20):
            self.errors.append(
                "Player name can only contain between 3 and 20 alphanumeric characters."
            )

        if Player.query.filter_by(name=player_name, game_key=game_key).first():
            self.errors.append(f"Player '{player_name}' already exists in session '{game_key}'.")

        return self

    def validate_state(self, state) -> Self:
        """Ensure correct state"""
        if not state == (current_state := games[self.data["game_key"]].status):
            self.errors.append(f"Invalid state: expected '{state}', but found '{current_state}'.")
        return self

    def validate_position(self) -> Self:
        position = int(self.data["position"])
        if not isinstance(position, int):
            self.errors.append("Position must be an integer.")
        return self
