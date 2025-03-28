import threading
from typing import Any

import numpy as np

from game.market import Market


class Exchange:
    """
    Manages interactions with the market.

    Uses a conditional to ensure that no trades or updates are made while the market is updating.
    """

    def __init__(self, market: Market) -> None:
        self.accounts: dict[str, dict[str, Any]] = {}
        self.market: Market = market
        self.sum_log_return: float = 0
        self.start_price: float = 100

        self.condition = threading.Condition()
        self.updating: bool = False

        self.market.reference_players(self.accounts)

    def add_player_account(self, player_key: str) -> None:
        self.accounts[player_key] = {
            "positions": np.zeros(self.market.epochs + 1, dtype=float),
            "leverage": 0,
        }

    def update_market(self) -> None:
        with self.condition:
            while self.updating:
                self.condition.wait()
            self.updating = True
            self.sum_log_return += self.market.update_state()
            self.updating = False
            self.condition.notify_all()

    def get_latest_price(self) -> tuple[int, float]:
        with self.condition:
            while self.updating:
                self.condition.wait()
            return self.market.epoch, np.exp(self.sum_log_return) * self.start_price

    def trade(self, player_key: str, position: int) -> tuple[int, int]:
        with self.condition:
            while self.updating:
                self.condition.wait()
            if abs(self.accounts[player_key]["leverage"] + position) <= 10:
                self.accounts[player_key]["positions"][self.market.epoch + 1] = position
                self.accounts[player_key]["leverage"] += position
            return self.market.epoch, self.accounts[player_key]["leverage"]


if __name__ == "__main__":
    market = Market(epochs=10)
    exchange = Exchange(market)
    exchange.add_player_account("player1")
    exchange.add_player_account("player2")
    exchange.add_player_account("player3")
    exchange.update_market()
    exchange.trade("player1", 10)
    exchange.update_market()
    exchange.trade("player2", -5)
    exchange.update_market()
    exchange.trade("player3", 15)
    exchange.update_market()
    epoch, price = exchange.get_latest_price()
    print(f"Epoch: {epoch}, Price: {price}")
    for key, value in exchange.accounts.items():
        print(key, value)
