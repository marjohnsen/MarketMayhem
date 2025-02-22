from protocols import MarketSimulatorProtocol
from typing import Any, Tuple
import numpy as np

# TODO: Change the market protocol to take the whole player dict
# TODO: This will increase the flexibility of the market simulator
# Use a dict to reference the position and leverage to enable fast lookup
# but also use a numpy array to store the same reference to positoin/leverage for fast iteration
# options 1: store keys in a dict and iterate over the keys looking up the dict
# option 2: you don't care about knowing the players, just the positions and leverage data.
#           can then use a numpy array to store the references to the positions and leverage.


class GameEngine:
    def __init__(self, simulator: MarketSimulatorProtocol, duration: int) -> None:
        if not isinstance(simulator, MarketSimulatorProtocol):
            raise TypeError(f"simulator must implement MarketSimulatorProtocol, got {type(simulator)}")
        self.sim: MarketSimulatorProtocol = simulator
        self.players: dict[str, dict[str, Any]] = {}
        self.duration: int = duration

    def add_player(self, player_key: str) -> None:
        self.players[player_key] = {
            "positions": np.full(self.duration + 1, np.nan, dtype=float),
            "leverage": 0,
        }

    def update_market(self) -> Tuple[float, float]:
        buy_volume, sell_volume = 0, 0
        for player in self.players.values():
            position = player["positions"][self.sim.epoch]
            buy_volume += position if position > 0 else 0
            sell_volume -= position if position < 0 else 0

        self.sim.update_market(buy_volume, sell_volume)
        return self.sim.price[self.sim.epoch], self.sim.log_return[self.sim.epoch]

    def trade(self, player_key: str, position: int) -> None:
        self.players[player_key]["leverage"] += position
        self.players[player_key]["positions"][self.sim.epoch + 1] = position


if __name__ == "__main__":
    from gaussian_market_simulator import GaussianMarketSimulator

    simulator = GaussianMarketSimulator(epochs=10, initial_price=100, volatility=0.1, decay=0.01)
    engine = GameEngine(simulator, 10)

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
