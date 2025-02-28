import inspect
from abc import ABC, ABCMeta, abstractmethod
from typing import Dict, Any

import numpy as np


class MarketSimulatorMeta(ABCMeta):
    """
    Enforces the implementation of specific behaviors in methods required by MarketSimulatorInterface.
    - requires `update_state` method to update `self.log_return[self.epoch]`
    - requires `update_state` method to increment `self.epoch`
    """

    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)

        if cls.__abstractmethods__:
            return cls

        if "update_state" in namespace:
            method_source = inspect.getsource(namespace["update_state"])

            if "self.log_return[self.epoch] = " not in method_source:
                raise TypeError(f"{name}.update_state must update `self.log_return[self.epoch]`.")

            if "self.epoch += 1" not in method_source and "self.epoch = self.epoch + 1" not in method_source:
                raise TypeError(f"{name}.update_state must increment `self.epoch`.")

        return cls


class MarketSimulatorInterface(ABC, metaclass=MarketSimulatorMeta):
    """Defines required methods and attributes for a market simulator."""

    @abstractmethod
    def __init__(self, epochs: int) -> None:
        """Required to initialize the market simulator"""
        self.epoch: int = 0
        self.epochs: int = epochs
        self.players: Dict[str, Dict[str, Any]]
        self.log_return: np.ndarray = np.empty(epochs + 1, dtype=float)

    @abstractmethod
    def reference_players(self, players: Dict[str, Dict[str, Any]]) -> None:
        """Required method to reference the players from the game engine."""
        self.players = players

    @abstractmethod
    def update_state(self) -> None:
        """Required method to update the market state. Expected to update log_return[self.epoch] and increment epoch."""
        pass
