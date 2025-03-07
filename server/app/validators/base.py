from typing import Any, Dict, List, Self

from flask import abort, current_app, jsonify

from app.db import db
from app.models import Player, Session


class BaseValidator:
    """Base class for route-specific validators."""

    def __init__(self, data: Dict[str, Any]):
        """Initialize the validator with the request data."""
        self.data: Dict[str, Any] = data
        self.errors: List[str] = []

    def require_fields(self, required_fields: list) -> Self:
        """Ensure all required fields are present and not empty."""
        missing = [field for field in required_fields if not self.data.get(field)]
        if missing:
            abort(jsonify({"Missing fields": f"{', '.join(missing)}"}), 400)
        return self

    def check_errors(self) -> Self:
        """Return all collected errors if any exist."""
        if self.errors:
            abort(jsonify({"error": "Validation failed", "details": self.errors}), 400)
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
