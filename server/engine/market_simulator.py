import numpy as np


def get_next_price(
    last_price: float, volatility: float, buy_volume: int, sell_volume: int
) -> float:
    """
    Simulate the next log return and update the price based on user input data
    and random noise.

    The simulated price is positively correlated with the net order flow.
    This means that the price will tend to increase when the buy volume
    is greater than the sell volume (positive net order flow), and
    decrease when the sell volume is greater than the buy volume
    (negative net order flow).

    Furthermore, volatility is negatively correlated with the trading
    volume. This means that price fluctuations are more pronounced when
    trading volume is low, and less volatile when trading volume is high.

    Parameters:
    last_price (float): The last known price.
    log_return_scale (float): The standard deviation of the log return.
    buy_volume (int): Total buy (long) volume.
    sell_volume (int): Total sell (short) volume.

    Returns:
    float: The next price.
    """
    trading_volume = max(buy_volume + sell_volume, 1)
    net_order_flow = buy_volume - sell_volume

    mean_log_return = volatility * (net_order_flow / trading_volume)
    std_log_return = volatility / np.sqrt(trading_volume)

    log_return = np.random.normal(mean_log_return, std_log_return)
    next_price = last_price * np.exp(log_return)

    return next_price


def get_price_series(last_price, volatility, buy_volume, sell_volume, N):
    if N == 0:
        return []
    next_price = get_next_price(last_price, volatility, buy_volume, sell_volume)
    return [last_price] + get_price_series(
        next_price, volatility, buy_volume, sell_volume, N - 1
    )


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # parameters
    last_price = 100
    volatility = 0.01
    buy_volume = 1
    sell_volume = 100
    N = 10

    price_series = get_price_series(last_price, volatility, buy_volume, sell_volume, N)

    plt.plot(price_series)
    plt.title("Generated Price Sequence (100 Steps)")
    plt.xlabel("Step")
    plt.ylabel("Price")
    plt.show()
