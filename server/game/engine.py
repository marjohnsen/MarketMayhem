from typing import Any, Type

import numpy as np
from game.market_simulators.interface import MarketSimulatorInterface

import os
import inspect
import importlib.util


class Exchange:
    def __init__(self, market_simulator: MarketSimulatorInterface, duration: int) -> None:
        self.duration: int = duration
        self.players: dict[str, dict[str, Any]] = {}
        self.market: MarketSimulatorInterface = market_simulator
        self.market.reference_players(self.players)

    def add_player(self, player_key: str) -> None:
        self.players[player_key] = {
            "positions": np.full(self.duration + 1, np.nan, dtype=float),
            "leverage": 0,
        }

    def trade(self, player_key: str, position: int) -> None:
        self.players[player_key]["positions"][self.market.epoch + 1] = position
        self.players[player_key]["leverage"] += position


class SimulatorCatalog:
    def __init__(self) -> None:
        self._classes = {}
        self._populate()

    def _populate(self) -> None:
        folder = os.path.join(os.path.dirname(__file__), "market_simulators")
        for fname in os.listdir(folder):
            if fname.endswith(".py") and not fname.startswith("__"):
                module_path = os.path.join(folder, fname)
                spec = importlib.util.spec_from_file_location(fname[:-3], module_path)
                if spec is None or spec.loader is None:
                    return
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for name, cls in inspect.getmembers(module, inspect.isclass):
                    if cls.__module__ == module.__name__ and issubclass(cls, MarketSimulatorInterface):
                        self._classes[name] = cls

    def __getitem__(self, key: str) -> type:
        return self._classes[key]

    def __iter__(self):
        return iter(self._classes)

    def __len__(self) -> int:
        return len(self._classes)

    def __repr__(self) -> str:
        return f"{list(self._classes.keys())}"


if __name__ == "__main__":
    catalog = SimulatorCatalog()
    list_of_all_available = list(catalog)
    print("Available simulators:", list_of_all_available)

    try:
        SimulatorClass = catalog["FractalMarketSimulator"]
        print("Fetched SimulatorClass:", SimulatorClass)
    except KeyError:
        print("Requested simulator not found")
        SimulatorClass = None

    try:
        SimulatorClass = catalog["GaussianMarketSimulator"]
        print("Fetched SimulatorClass:", SimulatorClass)
    except KeyError:
        print("Requested simulator not found")
        SimulatorClass = None

    if SimulatorClass is None:
        print("No simulator found")
        exit()

    market_simulator = SimulatorClass(epochs=10, volatility=0.1, decay=0.01)
    exchange = Exchange(market_simulator, 10)

    exchange.add_player("player1")
    exchange.add_player("player2")
    exchange.market.update_state()
    exchange.trade("player1", 1)
    exchange.trade("player2", -1)
    exchange.market.update_state()
    exchange.trade("player1", 2)
    exchange.trade("player2", 2)
    exchange.market.update_state()
    print(exchange.players["player1"])
    print(exchange.players["player2"])
