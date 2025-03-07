from app.validators.base import BaseValidator
from app.models import PlayerState, Player
from app.db import db
from typing import Self


class AdminValidator(BaseValidator):
    def validate_epochs(self) -> Self:
        """Ensure epochs is an int and within the required range."""
        epochs = self.data.get("epochs")

        if not isinstance(epochs, int):
            self.errors.append("Epochs must be an integer")
            return self

        if not (60 <= epochs <= 600):
            self.errors.append("Epochs must be an integer between 60 and 600")
        return self

    def validate_active_players(self) -> Self:
        """Ensure at least one active (connected) player exists in the session."""
        session_key = self.data.get("session_key")

        if not db.session.query(Player).filter_by(session_id=session_key, state=PlayerState.CONNECTED).count():
            self.errors.append("Cannot start the game with no connected players.")

        return self

    def validate_new_state(self) -> Self:
        new_state = self.data.get("new_state")
        valid_states = {state.value for state in PlayerState}
        if new_state not in valid_states:
            self.errors.append(f"Invalid state '{new_state}'. Must be one of {list(valid_states)}")
