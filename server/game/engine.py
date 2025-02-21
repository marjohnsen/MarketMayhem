from market_simulator import MarketSimulator
from typing import Any, Tuple
import numpy as np


class GameEngine:
    def __init__(self, duration: int, initial_price: float, volatility: float, decay: float) -> None:
        self.sim: MarketSimulator = MarketSimulator(duration, initial_price, volatility, decay)
        self.players: dict[str, dict[str, Any]] = {}
        self.duration: int = duration

    def add_player(self, player_key: str) -> None:
        self.players[player_key] = {
            "positions": np.full(self.duration + 1, np.nan, dtype=float),
            "leverage": 0,
        }

    def get_next_price(self) -> Tuple[float, float]:
        buy_volume, sell_volume = 0, 0
        for player in self.players.values():
            position = player["positions"][self.sim.epoch]
            buy_volume += position if position > 0 else 0
            sell_volume -= position if position < 0 else 0

        self.sim.get_next_price(buy_volume, sell_volume)
        return self.sim.price[self.sim.epoch], self.sim.log_return[self.sim.epoch]

    def trade(self, player_key: str, position: int) -> None:
        self.players[player_key]["leverage"] += position
        self.players[player_key]["positions"][self.sim.epoch + 1] = position


if __name__ == "__main__":
    engine = GameEngine(10, 100, 0.1, 0.01)
    engine.add_player("player1")
    engine.add_player("player2")
    engine.get_next_price()
    engine.trade("player1", 1)
    engine.trade("player2", -1)
    engine.get_next_price()
    engine.trade("player1", 2)
    engine.trade("player2", 2)
    engine.get_next_price()
    print(engine.players)
