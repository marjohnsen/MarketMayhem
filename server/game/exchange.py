import threading
from typing import Any

import numpy as np
from market import Market


class Exchange:
    """Manages interactions with the market."""

    def __init__(self, market: Market) -> None:
        self.accounts: dict[str, dict[str, Any]] = {}
        self.market: Market = market
        self.sum_log_return: float = 0
        self.start_price: float = 100

        self.condition = threading.Condition()
        self.updating: bool = False

        self.market.reference_players(self.accounts)

    def add_player_account(self, player_key: str) -> None:
        """Adds a player account to the exchange."""
        self.accounts[player_key] = {
            "positions": np.full(self.market.epochs + 1, np.nan, dtype=float),
            "leverage": 0,
        }

    def update_market(self) -> None:
        """Updates the market state."""
        with self.condition:
            while self.updating:
                self.condition.wait()
            self.updating = True
            self.sum_log_return += self.market.update_state()
            self.updating = False
            self.condition.notify_all()

    def trade(self, player_key: str, position: int) -> None:
        """Executes a trade and update the player account."""
        with self.condition:
            while self.updating:
                self.condition.wait()
            self.accounts[player_key]["positions"][self.market.epoch + 1] = position
            self.accounts[player_key]["leverage"] += position

    def get_latest_price(self) -> tuple[int, float]:
        with self.condition:
            while self.updating:
                self.condition.wait()
            return self.market.epoch, np.exp(self.sum_log_return) * self.start_price
