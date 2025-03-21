import re
from typing import Any, Dict, List, Self

from flask import abort, current_app, jsonify

from app.db import db
from app.models import Player, PlayerState, Session, SessionState
from game.simulators.catalog import SimulatorCatalog


class BaseValidators:
    """Base class for route-specific validators."""

    def __init__(self, data: Dict[str, Any]):
        """Initialize the validator with the request data."""
        self.data: Dict[str, Any] = data
        self.errors: List[str] = []

    def check_errors(self) -> Self:
        """Return all collected errors if any exist."""
        if self.errors:
            abort(jsonify({"error": "Validation failed", "details": self.errors}), 400)
        return self

    def require_fields(self, required_fields: list) -> Self:
        """Ensure all required fields are present and not empty."""
        missing = [field for field in required_fields if not self.data.get(field)]
        if missing:
            abort(jsonify({"Missing fields": f"{', '.join(missing)}"}), 400)
        return self

    def validate_admin_key(self) -> Self:
        """Check if the admin key is valid."""
        if self.data.get("admin_key") != current_app.config["ADMIN_KEY"]:
            self.errors.append("Invalid admin key.")
        return self

    def validate_session_key(self) -> Self:
        """Ensure the session exists."""
        session_key = self.data.get("session_key")
        if not db.session.query(Session).filter_by(key=session_key).first():
            self.errors.append(f"Session '{session_key}' not found.")
        return self

    def validate_player_key(self) -> Self:
        """Ensure the player exists in the session."""
        player_name = self.data.get("player_name")
        session_key = self.data.get("session_key")
        if not db.session.query(Player).filter_by(name=player_name, session_key=session_key).first():
            self.errors.append(f"Player '{player_name}' not found in session '{session_key}'.")
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
        session_obj = Session.query.filter_by(key=self.data.get("session_key")).first()
        if (
            not session_obj
            or db.session.query(Player).filter_by(session_id=session_obj.id, state=PlayerState.CONNECTED).count() == 0
        ):
            self.errors.append("Cannot start the game with no connected players.")
        return self

    def validate_new_state(self) -> Self:
        new_state = self.data.get("new_state")
        valid_states = {state.value for state in PlayerState}
        if new_state not in valid_states:
            self.errors.append(f"Invalid state '{new_state}'. Must be one of {list(valid_states)}")

        return self

    def validate_simulator(self) -> Self:
        simulator = self.data.get("simulator")
        if simulator not in SimulatorCatalog:
            self.errors.append(f"Simulator '{simulator}' does not eixt. Choose one of {list(SimulatorCatalog)}")
        return self


class LobbyValidators(BaseValidators):
    def validate_player_name(self) -> Self:
        player_name = str(self.data.get("player_name"))
        if not re.match(r"^[a-zA-Z0-9]+$", player_name) or not (3 <= len(player_name) <= 20):
            self.errors.append("Player name can only contain between 3 and 20 alphanumeric characters")
        session_key = self.data.get("session_key")
        session = db.session.query(Session).filter_by(key=session_key).first()
        if existing_player := Player.query.filter_by(name=player_name, session_id=session.id).first():
            self.errors.append(f"Player '{existing_player.name}' already exists")
        return self

    def validate_state(self) -> Self:
        session_key = self.data.get("session_key")
        session = db.session.query(Session).filter_by(key=session_key).first()
        if session and session.state != SessionState.LOBBY:
            self.errors.append("The game has started and the lobby is closed.")
        return self
