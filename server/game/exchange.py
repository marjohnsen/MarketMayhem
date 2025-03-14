from typing import Any

import numpy as np
from game.simulators.interface import MarketSimulatorInterface

import threading


class Exchange:
    def __init__(self, market_simulator: MarketSimulatorInterface, duration: int) -> None:
        self.duration: int = duration
        self.players: dict[str, dict[str, Any]] = {}
        self.market: MarketSimulatorInterface = market_simulator
        self.market.reference_players(self.players)
        self.update_lock: threading.Lock = threading.Lock()
        self.trade_lock: threading.Lock = threading.Lock()

    def add_player(self, player_key: str) -> None:
        self.players[player_key] = {
            "positions": np.full(self.duration + 1, np.nan, dtype=float),
            "leverage": 0,
            "lock": threading.Lock(),
        }

    def trade(self, player_key: str, position: int) -> None:
        with self.trade_lock:
            with self.players[player_key]["lock"]:
                self.players[player_key]["positions"][self.market.epoch + 1] = position
                self.players[player_key]["leverage"] += position

    def update_market(self) -> None:
        with self.update_lock:
            with self.trade_lock:
                self.market.update_state()

    def get_latest_price(self) -> float:
        with self.trade_lock:
            return self.market.get_latest_price()
