import threading
from typing import Any

import numpy as np

from game.simulators.interface import MarketSimulatorInterface


class Exchange:
    def __init__(self, market_simulator: MarketSimulatorInterface) -> None:
        self.players: dict[str, dict[str, Any]] = {}
        self.market: MarketSimulatorInterface = market_simulator
        self.sum_log_return: float = 0
        self.start_price: float = 100
        self.lock: threading.Lock = threading.Lock()
        self.market.reference_players(self.players)

    def add_player(self, player_key: str) -> None:
        self.players[player_key] = {
            "positions": np.full(self.market.epochs + 1, np.nan, dtype=float),
            "leverage": 0,
        }

    def trade(self, player_key: str, position: int) -> None:
        with self.lock:
            self.players[player_key]["positions"][self.market.epoch + 1] = position
            self.players[player_key]["leverage"] += position

    def update_market(self) -> None:
        with self.lock:
            self.sum_log_return += self.market.update_state()

    def get_latest_price(self) -> tuple[int, float]:
        with self.lock:
            return self.market.epoch, np.exp(self.sum_log_return) * self.start_price
