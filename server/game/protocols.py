from typing import Protocol, runtime_checkable
import numpy as np


@runtime_checkable
class MarketSimulatorProtocol(Protocol):
    epoch: int
    price: np.ndarray
    log_return: np.ndarray

    def update_market(self, buy_volume: int, sell_volume: int) -> None: ...
