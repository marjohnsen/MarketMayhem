import numpy as np
from datetime import datetime


class MarketSimulator:
    def __init__(self, epochs: int, initial_price: float = 100.0, volatility: float = 0.01, decay: float = 0.7) -> None:
        # Parameters
        self.epochs = epochs
        self.volatility = volatility
        self.decay = decay
        self.epoch = 0

        # Simulation states
        self.trading_volume = np.empty(epochs + 1, dtype=float)
        self.order_flow = np.empty(epochs + 1, dtype=float)
        self.jitter = np.empty(epochs + 1, dtype=float)
        self.surge = np.empty(epochs + 1, dtype=float)
        self.dispersion = np.empty(epochs + 1, dtype=float)
        self.sentiment = np.empty(epochs + 1, dtype=float)

        # Simulation output
        self.log_return = np.empty(epochs + 1, dtype=float)
        self.price = np.empty(epochs + 1, dtype=float)
        self.datetime = np.empty(epochs + 1, dtype=object)

        # Initialize
        self.trading_volume[0] = 0.0
        self.order_flow[0] = 0.0
        self.jitter[0] = 0.0
        self.surge[0] = 0.0
        self.dispersion[0] = 0.0
        self.sentiment[0] = 0.0
        self.log_return[0] = 0.0
        self.price[0] = initial_price
        self.get_next_price = self._initialize_simulator

    def _initialize_simulator(self, buy_volume: int, sell_volume: int) -> None:
        self.datetime[0] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.get_next_price = self._next_price

    def _next_price(self, buy_volume: int, sell_volume: int) -> None:
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
        price = self.price[self.epoch] * np.exp(log_return)

        # Update market state
        self.epoch = self.epoch + 1
        self.trading_volume[self.epoch] = trading_volume
        self.order_flow[self.epoch] = order_flow
        self.jitter[self.epoch] = jitter
        self.surge[self.epoch] = surge
        self.dispersion[self.epoch] = dispersion
        self.sentiment[self.epoch] = sentiment
        self.log_return[self.epoch] = log_return
        self.price[self.epoch] = price
        self.datetime[self.epoch] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # Simulate trades
    trades = []
    n_simulations = 200
    buy_pattern = [0.25] * 16 + [0.5] * 16 + [0.75] * 16
    trade_pattern = [1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2]

    for i in range(n_simulations + 1):
        n_trades = trade_pattern[i % len(trade_pattern)]
        buy_fraction = buy_pattern[i % len(buy_pattern)]
        n_buys = int(round(n_trades * buy_fraction))
        trades.append((n_buys, n_trades - n_buys))

    # Simulate market
    simulator = MarketSimulator(n_simulations)
    for n_buys, n_sells in trades:
        simulator.get_next_price(n_buys, n_sells)

    # Create subplots
    fig, axs = plt.subplots(4, 2, figsize=(10, 15))
    plots = [
        (simulator.trading_volume[1:], "Trading Volumes", "plot"),
        (simulator.order_flow[1:], "Order Flows", "plot"),
        (simulator.jitter[1:], "Jitters", "plot"),
        (simulator.surge[1:], "Surges", "plot"),
        (simulator.dispersion[1:], "Dispersions", "plot"),
        (simulator.sentiment[1:], "Sentiments", "plot"),
        (simulator.log_return[1:], "Log Returns", "hist"),
        (simulator.price[1:], "Prices", "plot"),
    ]

    for ax, (data, title, plot_type) in zip(axs.flat, plots):
        if plot_type == "hist":
            ax.hist(data, bins=20, alpha=0.5)
        else:
            ax.plot(data)
        ax.set_title(title)

    plt.tight_layout()
    plt.show()
