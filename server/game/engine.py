import time
from typing import List
from game.exchange import Exchange
from game.simulators.catalog import SimulatorCatalog


class GameEngine:
    def __init__(self, player_keys: List[str], simulator: str, epochs: int, timestep: int) -> None:
        self.running = False
        self.epochs = epochs
        self.timestep = timestep
        self.simulator = simulator

        market = SimulatorCatalog[simulator]
        self.exchange = Exchange(market, epochs)

        for key in player_keys:
            self.exchange.add_player(key)

    def run(self):
        self.running = True
        while self.running:
            time.sleep(((self.timestep - 0.1) - (time.time() % self.timestep)) % self.timestep)
            self.exchange.market.update_state()

    def stop(self):
        self.running = False
