import threading
from typing import Any

import numpy as np

from game.market import Market


class Exchange:
    """
    Manages interactions with the market.
    """

    def __init__(self, market: Market) -> None:
        self.accounts: dict[str, dict[str, Any]] = {}
        self.market: Market = market
        self.sum_log_return: float = 0
        self.start_price: float = 100

        self.lock: threading.Lock = threading.Lock()

        self.market.reference_players(self.accounts)

    def add_player_account(self, player_key: str) -> None:
        self.accounts[player_key] = {
            "positions": np.zeros(self.market.epochs + 1, dtype=float),
            "leverage": 0,
        }

    def update_market(self) -> None:
        with self.lock:
            self.sum_log_return += self.market.update_state()

    def get_latest_price(self) -> tuple[int, float]:
        with self.lock:
            return self.market.epoch, np.exp(self.sum_log_return) * self.start_price

    def trade(self, player_key: str, position: int) -> tuple[int, int]:
        with self.lock:
            if abs(self.accounts[player_key]["leverage"] + position) <= 10:
                self.accounts[player_key]["positions"][self.market.epoch + 1] = position
                self.accounts[player_key]["leverage"] += position
            return self.market.epoch, self.accounts[player_key]["leverage"]
