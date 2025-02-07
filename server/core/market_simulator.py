import numpy as np
import matplotlib.pyplot as plt


class MarketSimulator:
    def __init__(
        self,
        initial_price: float,
        volatility: float,
        memory_decay: float = 0.9,
        momentum_factor: float = 0.1,
        long_term_volatility_factor: float = 0.5,
    ):
        """
        Parameters:
        -----------
        initial_price : float
            The starting price of the asset.
        volatility : float
            A baseline measure of price volatility.
        memory_decay : float, optional
            The decay rate for the long-term memory (between 0 and 1). A value close to 1 means
            that past order flows persist longer.
        momentum_factor : float, optional
            Scales the impact of the long-term memory on the mean log return (market inertia).
        long_term_volatility_factor : float, optional
            Scales the impact of the long-term memory on volatility (uncertainty). A higher value
            increases the standard deviation when persistent order flows are present.
        """
        self.price = initial_price
        self.volatility = volatility
        self.memory_decay = memory_decay
        self.momentum_factor = momentum_factor
        self.long_term_volatility_factor = long_term_volatility_factor
        self.accumulated_flow = 0.0

    def update_price(self, buy_volume: int, sell_volume: int) -> float:
        """
        Update the price based on current trading volumes and the memory of past order flow.

        Parameters:
        -----------
        buy_volume : int
            Total buy volume in the current period.
        sell_volume : int
            Total sell volume in the current period.

        Returns:
        --------
        float
            The updated price.
        """
        trading_volume = max(buy_volume + sell_volume, 1)
        net_order_flow = buy_volume - sell_volume
        normalized_flow = net_order_flow / trading_volume

        self.accumulated_flow = (
            self.memory_decay * self.accumulated_flow
            + (1 - self.memory_decay) * normalized_flow
        )

        # Short-term impact: immediate effect of the current normalized order flow.
        # Long-term impact: the persistent effect (market inertia or momentum).
        short_term_impact = self.volatility * normalized_flow
        long_term_impact = self.momentum_factor * self.accumulated_flow
        mean_log_return = short_term_impact + long_term_impact

        # The volatility is adjusted based on long-term memory.
        # High accumulated flow tend to increase uncertainty.
        adjusted_volatility = self.volatility * (
            1 + self.long_term_volatility_factor * abs(self.accumulated_flow)
        )
        std_log_return = adjusted_volatility / np.sqrt(trading_volume)

        # Update price
        log_return = np.random.normal(mean_log_return, std_log_return)
        self.price *= np.exp(log_return)
        return self.price

    def generate_price_series(self, buy_volume: int, sell_volume: int, steps: int):
        """
        Generate a series of prices over a number of time steps.

        Parameters:
        -----------
        buy_volume : int
            The buy volume (can be varied over time if desired).
        sell_volume : int
            The sell volume.
        steps : int
            Number of time steps to simulate.

        Returns:
        --------
        list of float
            The series of simulated prices.
        """
        prices = [self.price]
        for _ in range(steps):
            new_price = self.update_price(buy_volume, sell_volume)
            prices.append(new_price)
        return prices


if __name__ == "__main__":
    # Simulation parameters
    initial_price = 100.0
    volatility = 0.01
    memory_decay = 0.95  # Longer memory: past order flows persist
    momentum_factor = 0.05  # Influence of long-term memory on drift
    long_term_volatility_factor = 0.5  # Influence of long-term memory on volatility
    buy_volume = 1
    sell_volume = 100
    steps = 100

    simulator = MarketSimulator(
        initial_price,
        volatility,
        memory_decay,
        momentum_factor,
        long_term_volatility_factor,
    )
    price_series = simulator.generate_price_series(buy_volume, sell_volume, steps)

    plt.figure(figsize=(10, 5))
    plt.plot(price_series, marker="o")
    plt.title(
        "Simulated Price Series with Long-Term Memory on Both Drift and Volatility"
    )
    plt.xlabel("Time Step")
    plt.ylabel("Price")
    plt.grid(True)
    plt.show()

