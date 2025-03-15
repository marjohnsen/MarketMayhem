import time
from typing import List
from game.exchange import Exchange
from game.simulators.catalog import SimulatorCatalog


class GameEngine:
    """
    Orchestrates all the game loop and all the game components.

    Attributes:
        running (bool): Indicates if the game engine is running.
        epochs (int): Number of epochs the game will run.
        timestep (int): Time interval between each epoch.
        simulator (str): Name of the simulator.
        exchange (Exchange): Manages the player interaction with the market.
    """

    def __init__(self, player_keys: List[str], simulator: str, epochs: int, timestep: int) -> None:
        self.running = False
        self.timestep = timestep
        self.simulator = simulator

        Simulator = SimulatorCatalog[simulator]
        market = Simulator(epochs)
        self.exchange = Exchange(market)

        for key in player_keys:
            self.exchange.add_player(key)

    def run(self):
        self.running = True
        while self.exchange.market.epoch <= self.exchange.market.epochs and self.running:
            time.sleep(((self.timestep - 0.1) - (time.time() % self.timestep)) % self.timestep)
            self.exchange.market.update_state()

    def stop(self):
        self.running = False
