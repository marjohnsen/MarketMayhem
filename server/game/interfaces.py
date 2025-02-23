from abc import ABC, abstractmethod
from typing import Union
import numpy as np


class MarketSimulatorInterface(ABC):
    def __init__(self, epochs: int, players: dict[str, dict[str, Union[np.ndarray, int]]]) -> None:
        self.epoch: int = 0
        self.epochs: int = epochs
        self.players: dict[str, dict[str, Union[np.ndarray, int]]] = players
        self.log_return: np.ndarray = np.empty(0)

    @abstractmethod
    def reference_players(self, players: dict[str, dict[str, Union[np.ndarray, int]]]) -> None:
        self.players = players

    @abstractmethod
    def update_market(self) -> None:
        pass
