import numpy as np
from game.simulators.interface import MarketSimulatorInterface


class GaussianMarketSimulator(MarketSimulatorInterface):
    def __init__(self, epochs: int, volatility: float = 0.01, decay: float = 0.7) -> None:
        # Initialize parent class
        super().__init__(epochs)

        # Parameters
        self.volatility = volatility
        self.decay = decay

        # Simulation states
        self.trading_volume = np.empty(epochs + 1, dtype=float)
        self.order_flow = np.empty(epochs + 1, dtype=float)
        self.jitter = np.empty(epochs + 1, dtype=float)
        self.surge = np.empty(epochs + 1, dtype=float)
        self.dispersion = np.empty(epochs + 1, dtype=float)
        self.sentiment = np.empty(epochs + 1, dtype=float)

        # Initialize
        self.trading_volume[self.epoch] = 0.0
        self.order_flow[self.epoch] = 0.0
        self.jitter[self.epoch] = 0.0
        self.surge[self.epoch] = 0.0
        self.dispersion[self.epoch] = 0.0
        self.sentiment[self.epoch] = 0.0
        self.log_return[self.epoch] = 0.0

    def update_state(self) -> float:
        # Compute trading volume
        buy_volume, sell_volume = 0, 0
        for player in self.players.values():
            position = player["positions"][self.epoch]
            buy_volume += position if position > 0 else 0
            sell_volume -= position if position < 0 else 0

        # calculate market metrics
        trading_volume = buy_volume + sell_volume
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

        return self.log_return[self.epoch]


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    simulator = GaussianMarketSimulator(100)
    players = {"player1": {"positions": np.zeros(102), "leverage": 0}}
    simulator.reference_players(players)

    while simulator.epoch < simulator.epochs:
        simulator.update_state()

    arrays = [
        (simulator.trading_volume, "Trading Volume"),
        (simulator.order_flow, "Order Flow"),
        (simulator.jitter, "Jitter"),
        (simulator.surge, "Surge"),
        (simulator.dispersion, "Dispersion"),
        (simulator.sentiment, "Sentiment"),
        (simulator.log_return, "Log Return"),
        (100 * np.exp(np.cumsum(simulator.log_return)), "Price"),
    ]

    fig, axs = plt.subplots(nrows=len(arrays), ncols=1, sharex=True, figsize=(10, 15))
    for ax, (arr, label) in zip(axs, arrays):
        ax.plot(arr, label=label)
        ax.set_ylabel(label)
        ax.legend(loc="upper right")

    axs[-1].set_xlabel("Epoch")
    plt.tight_layout()
    plt.show()
