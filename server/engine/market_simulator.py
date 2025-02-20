import numpy as np


class MarketSimulator:
    def __init__(self, epochs: int, initial_price: float = 100.0, volatility: float = 0.01, decay: float = 0.7) -> None:
        self.epochs = epochs
        self.volatility = volatility
        self.decay = decay
        self.epoch = 0

        self.trading_volume = np.zeros(epochs, dtype=float)
        self.order_flow = np.zeros(epochs, dtype=float)
        self.trading_volume_ratio = np.zeros(epochs, dtype=float)
        self.order_flow_ratio = np.zeros(epochs, dtype=float)
        self.jitter = np.zeros(epochs, dtype=float)
        self.surge = np.zeros(epochs, dtype=float)
        self.dispersion = np.zeros(epochs, dtype=float)
        self.sentiment = np.zeros(epochs, dtype=float)
        self.log_return = np.zeros(epochs, dtype=float)
        self.price = np.zeros(epochs, dtype=float)

        self.price[0] = initial_price

    def get_next_price(self, buy_volume: int, sell_volume: int) -> None:
        trading_volume = buy_volume + sell_volume or 1
        order_flow = buy_volume - sell_volume

        current_tv = self.trading_volume[: self.epoch]
        nonzero_tv = current_tv[current_tv != 0]
        volume_percentile = np.percentile(nonzero_tv, 90) if nonzero_tv.size > 0 else 1.0

        trading_volume_ratio = np.minimum(trading_volume / volume_percentile, 1)
        order_flow_ratio = np.clip(order_flow / volume_percentile, -1, 1)

        jitter = self.volatility * (1 - trading_volume_ratio)
        surge = self.volatility * order_flow_ratio

        dispersion = self.dispersion[self.epoch] * self.decay + jitter * (1 - self.decay)
        sentiment = self.sentiment[self.epoch] * self.decay + surge * (1 - self.decay)

        log_return = np.random.normal(surge + sentiment, jitter + dispersion)
        price = self.price[self.epoch] * np.exp(log_return)

        self.epoch = self.epoch + 1
        self.trading_volume[self.epoch] = trading_volume
        self.order_flow[self.epoch] = order_flow
        self.trading_volume_ratio[self.epoch] = trading_volume_ratio
        self.order_flow_ratio[self.epoch] = order_flow_ratio
        self.jitter[self.epoch] = jitter
        self.surge[self.epoch] = surge
        self.dispersion[self.epoch] = dispersion
        self.sentiment[self.epoch] = sentiment
        self.log_return[self.epoch] = log_return
        self.price[self.epoch] = price


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # Simulate trades
    trades = []
    prev_trades = 0
    for _ in range(99):
        lam = 2 + 0.3 * prev_trades
        n_trades = np.random.poisson(lam)
        n_buys = np.random.binomial(n_trades, 0.5)
        trades.append((n_buys, n_trades - n_buys))
        prev_trades = n_trades

    # Simulate market
    simulator = MarketSimulator(100)
    for n_buys, n_sells in trades:
        simulator.get_next_price(n_buys, n_sells)

    # Create subplots
    fig, axs = plt.subplots(5, 2, figsize=(10, 15))
    plots = [
        (simulator.trading_volume[1:], "Trading Volumes", "plot"),
        (simulator.order_flow[1:], "Order Flows", "plot"),
        (simulator.trading_volume_ratio[1:], "Trading Volume Ratios", "plot"),
        (simulator.order_flow_ratio[1:], "Order Flow Ratios", "plot"),
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

    print("total variance of log returns:", np.std(simulator.log_return[1:]))
    plt.tight_layout()
    plt.show()
