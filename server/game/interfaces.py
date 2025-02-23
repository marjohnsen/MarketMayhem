from abc import ABC, ABCMeta, abstractmethod
from typing import Dict, Union
import numpy as np
import inspect


class MarketSimulatorMeta(ABCMeta):
    """
    Metaclass enforcing the MarketSimulatorInterface protocol:
    - requires `update_market` method to update `self.log_return[self.epoch]`
    - requires `update_market` method to increment `self.epoch`
    """

    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)

        if "update_market" in namespace:
            method_source = inspect.getsource(namespace["update_market"])

            if "self.log_return[self.epoch] = " not in method_source:
                raise TypeError(f"{name}.update_market must update `self.log_return[self.epoch]`.")

            if "self.epoch += 1" not in method_source and "self.epoch = self.epoch + 1" not in method_source:
                raise TypeError(f"{name}.update_market must increment `self.epoch`.")

        return cls


class MarketSimulatorInterface(ABC, metaclass=MarketSimulatorMeta):
    """Defines the interface for market simulators"""

    @abstractmethod
    def __init__(self, epochs: int) -> None:
        """Required to initialize the market simulator"""
        self.epoch: int = 0
        self.epochs: int = epochs
        self.players: Dict[str, Dict[str, Union[np.ndarray, int]]]
        self.datetime: np.ndarray = np.empty(epochs + 1, dtype=float)
        self.log_return: np.ndarray = np.empty(epochs + 1, dtype=float)

    @abstractmethod
    def reference_players(self, players: Dict[str, Dict[str, Union[np.ndarray, int]]]) -> None:
        """Required method to reference the players from the game engine."""
        self.players = players

    @abstractmethod
    def update_market(self) -> None:
        """Required method to update the market state. Expected to update log_return[self.epoch] and increment epoch."""
        pass
