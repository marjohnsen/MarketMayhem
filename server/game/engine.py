from game.market_simulator import MarketSimulator
from datetime import datetime, timedelta
import time
import numpy as np


class GameEngine:
    def __init__(self, duration: int) -> None:
        self.duration = duration
        self.epoch = 0
        self.start_time = 0
        self.players = {}

    def add_player(self, player_key: str) -> None:
        self.players[player_key] = {"holdings": np.full(self.duration, np.nan, dtype=float)}

    def start_game(self, initial_price: float, volatility: float, decay: float) -> None:
        self.simulator = MarketSimulator(self.duration, initial_price, volatility, decay)

    def next_epoch(self, buy_volume: int, sell_volume: int) -> None:
        self.simulator.get_next_price(buy_volume, sell_volume)
        self.epoch += 1

    def trade(self, player_key: str, volume: int) -> None:
        self.players[player_key]["holdings"][self.epoch] = volume
