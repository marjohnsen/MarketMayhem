import numpy as np


class MarketSimulator:
    def __init__(self, session) -> None:
        self.session = session.L
        self.max_volume = session.players.count()


def get_next_price(last_price: float, volatility: float, buy_volume: int, sell_volume: int, max_volume: int) -> float:
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
    volatility (float): The standard deviation of the log return.
    buy_volume (int): Total buy (long) volume.
    sell_volume (int): Total sell (short) volume.

    Returns:
    float: The next price.
    """
    trading_volume = np.maximum(buy_volume + sell_volume, 1)
    trading_volume_ratio = trading_volume / max_volume
    order_flow_ratio = (buy_volume - sell_volume) / trading_volume

    short_term_drift = volatility * order_flow_ratio
    short_term_volatility = volatility * (1 - trading_volume_ratio)

    long_term_drift
    short_term_volatility

    log_return = np.random.normal(short_term_drift, short_term_volatility)
    next_price = last_price * np.exp(log_return)

    return next_price
