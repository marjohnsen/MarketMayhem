import numpy as np
from typing import List


class MarketSimulator:
    def __init__(self, initial_price: float, volatility: float, max_volume: int) -> None:
        self.DECAY: float = 0.7
        self.MAX_VOLUME: int = max_volume
        self.VOLATILITY: float = volatility

        self.trading_volumes: List[int] = [0]
        self.order_flows: List[int] = [0]
        self.trading_volume_ratios: List[float] = [0.0]
        self.order_flow_ratios: List[float] = [0.0]

        self.jitters: List[float] = [0.0]
        self.surges: List[float] = [0.0]

        self.dispersions: List[float] = [0.0]
        self.sentiments: List[float] = [0.0]

        self.log_returns: List[float] = [0.0]
        self.prices: List[float] = [initial_price]

    def get_next_price(self, buy_volume: int, sell_volume: int) -> None:
        trading_volume: int = buy_volume + sell_volume or 1
        order_flow: int = buy_volume - sell_volume
        trading_volume_ratio: float = trading_volume / self.MAX_VOLUME
        order_flow_ratio: float = order_flow / (self.MAX_VOLUME / 2)

        jitter: float = self.VOLATILITY * (1 - np.minimum(trading_volume_ratio / 0.1, 1))
        surge: float = self.VOLATILITY * np.minimum(order_flow_ratio / 0.2, 1)

        dispersion: float = self.dispersions[-1] * self.DECAY + jitter * (1 - self.DECAY)
        sentiment: float = self.sentiments[-1] * self.DECAY + surge * (1 - self.DECAY)

        log_return: float = np.random.normal(surge + sentiment, jitter + dispersion)
        next_price: float = self.prices[-1] * np.exp(log_return)

        self.trading_volumes.append(trading_volume)
        self.order_flows.append(order_flow)
        self.trading_volume_ratios.append(trading_volume_ratio)
        self.order_flow_ratios.append(order_flow_ratio)

        self.jitters.append(jitter)
        self.surges.append(surge)

        self.dispersions.append(dispersion)
        self.sentiments.append(sentiment)

        self.log_returns.append(log_return)
        self.prices.append(next_price)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    trades = []
    prev_trades = 0

    # Simulate trades
    for _ in range(100):
        lam = 2 + 0.3 * prev_trades
        n_trades = np.random.poisson(lam)
        n_buys = np.random.binomial(n_trades, 0.5)
        n_sells = n_trades - n_buys
        trades.append([n_buys, n_sells])
        prev_trades = n_trades

    # Simulate market
    simulator = MarketSimulator(100.0, 0.001, 200)

    for trade in trades:
        simulator.get_next_price(trade[0], trade[1])

    # Subplot of all series in class:
    fig, axs = plt.subplots(5, 2, figsize=(10, 15))
    axs[0, 0].plot(simulator.trading_volumes[1:])
    axs[0, 0].set_title("Trading Volumes")
    axs[0, 1].plot(simulator.order_flows[1:])
    axs[0, 1].set_title("Order Flows")
    axs[1, 0].plot(simulator.trading_volume_ratios[1:])
    axs[1, 0].set_title("Trading Volume Ratios")
    axs[1, 1].plot(simulator.order_flow_ratios[1:])
    axs[1, 1].set_title("Order Flow Ratios")
    axs[2, 0].plot(simulator.jitters[1:])
    axs[2, 0].set_title("Jitters")
    axs[2, 1].plot(simulator.surges[1:])
    axs[2, 1].set_title("Surges")
    axs[3, 0].plot(simulator.dispersions[1:])
    axs[3, 0].set_title("Dispersions")
    axs[3, 1].plot(simulator.sentiments[1:])
    axs[3, 1].set_title("Sentiments")
    axs[4, 0].hist(simulator.log_returns[1:], bins=20, alpha=0.5)
    axs[4, 0].set_title("Log Returns")
    axs[4, 1].plot(simulator.prices[1:])
    axs[4, 1].set_title("Prices")
    print(f"total variance of log returns: {np.std(simulator.log_returns[1:])}")
    plt.show()
