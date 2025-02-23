from typing import Any

import numpy as np
from interfaces import MarketSimulatorInterface


class GameEngine:
    def __init__(self, simulator: MarketSimulatorInterface, duration: int) -> None:
        self.duration: int = duration
        self.players: dict[str, dict[str, Any]] = {}
        if not isinstance(simulator, MarketSimulatorInterface):
            raise ValueError(f"simulator must implement MarketSimulatorInterface, got: {type(simulator)}")
        self.sim: MarketSimulatorInterface = simulator
        self.sim.reference_players(self.players)

    def add_player(self, player_key: str) -> None:
        self.players[player_key] = {
            "positions": np.full(self.duration + 1, np.nan, dtype=float),
            "leverage": 0,
        }

    def trade(self, player_key: str, position: int) -> None:
        self.players[player_key]["positions"][self.sim.epoch + 1] = position
        self.players[player_key]["leverage"] += position


if __name__ == "__main__":
    from gaussian_market_simulator import GaussianMarketSimulator

    simulator = GaussianMarketSimulator(epochs=10, volatility=0.1, decay=0.01)
    engine = GameEngine(simulator, 10)

    engine.add_player("player1")
    engine.add_player("player2")
    engine.sim.update_market()
    engine.trade("player1", 1)
    engine.trade("player2", -1)
    engine.sim.update_market()
    engine.trade("player1", 2)
    engine.trade("player2", 2)
    engine.sim.update_market()
    print(engine.players)
