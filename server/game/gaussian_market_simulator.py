from typing import Dict, Union

import numpy as np
from interfaces import MarketSimulatorInterface


class GaussianMarketSimulator(MarketSimulatorInterface):
    def __init__(self, epochs: int, volatility: float = 0.01, decay: float = 0.7) -> None:
        # Parameters
        self.epochs = epochs
        self.volatility = volatility
        self.decay = decay

        # Simulation states
        self.trading_volume = np.empty(epochs + 1, dtype=float)
        self.order_flow = np.empty(epochs + 1, dtype=float)
        self.jitter = np.empty(epochs + 1, dtype=float)
        self.surge = np.empty(epochs + 1, dtype=float)
        self.dispersion = np.empty(epochs + 1, dtype=float)
        self.sentiment = np.empty(epochs + 1, dtype=float)

        # Default attributes
        self.players: Dict[str, Dict[str, Union[np.ndarray, int]]] = {}
        self.log_return = np.empty(epochs + 1, dtype=float)

        # Initialize
        self.epoch = 0
        self.trading_volume[self.epoch] = 0.0
        self.order_flow[self.epoch] = 0.0
        self.jitter[self.epoch] = 0.0
        self.surge[self.epoch] = 0.0
        self.dispersion[self.epoch] = 0.0
        self.sentiment[self.epoch] = 0.0
        self.log_return[self.epoch] = 0.0

    def reference_players(self, players: Dict[str, Dict[str, Union[np.ndarray, int]]]) -> None:
        self.players = players

    def update_market(self) -> None:
        # Compute trading volume
        buy_volume, sell_volume = 0, 0
        for player in self.players.values():
            position = player["positions"][self.epoch]
            buy_volume += position if position > 0 else 0
            sell_volume -= position if position < 0 else 0

        # calculate market metrics
        trading_volume = buy_volume + sell_volume or 1
        order_flow = buy_volume - sell_volume

        # calculate percentile of trading volume
        current_tv = self.trading_volume[: self.epoch]
        nonzero_tv = current_tv[current_tv != 0]
        volume_percentile = np.percentile(nonzero_tv, 90) if nonzero_tv.size >= 3 else np.inf

        # calculate market ratios
        trading_volume_ratio = np.minimum(trading_volume / volume_percentile, 1)
        order_flow_ratio = np.clip(order_flow / volume_percentile, -1, 1)

        # calculate short term market effects
        jitter = self.volatility * (1 - trading_volume_ratio)
        surge = 0.5 * self.volatility * order_flow_ratio

        # calculate long term market effects
        dispersion = self.dispersion[self.epoch] * self.decay + jitter * (1 - self.decay)
        sentiment = self.sentiment[self.epoch] * self.decay + surge * (1 - self.decay)

        # simulate price
        log_return = np.random.normal(surge + sentiment, jitter + dispersion)

        # Update market state
        self.epoch += 1
        self.trading_volume[self.epoch] = trading_volume
        self.order_flow[self.epoch] = order_flow
        self.jitter[self.epoch] = jitter
        self.surge[self.epoch] = surge
        self.dispersion[self.epoch] = dispersion
        self.sentiment[self.epoch] = sentiment
        self.log_return[self.epoch] = log_return
