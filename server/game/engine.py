import time
from typing import List, Optional
from game.exchange import Exchange
from game.market import Market
import threading


class GameEngine:
    """Orchestrates the game loop."""

    def __init__(self, player_keys: List[str], simulator: str, epochs: int, timestep: int) -> None:
        """
        Initializes the game components.

        :param player_keys: List of player keys.
        :param simulator: The simulator to use.
        :param epochs: Number of epochs to run the game for.
        :param timestep: The time interval between each epoch.
        """
        self.timestep: int = timestep
        self.simulator: str = simulator
        self.running: bool = False
        self.updating: bool = False
        self.thread: Optional[threading.Thread] = None

        market = Market(epochs)
        self.exchange: Exchange = Exchange(market)

        for key in player_keys:
            self.exchange.add_player_account(key)

    def run(self) -> None:
        """Starts the game loop."""
        self.running = True
        while self.exchange.market.epoch <= self.exchange.market.epochs and self.running:
            time.sleep(((self.timestep - 0.1) - (time.time() % self.timestep)) % self.timestep)
            self.exchange.update_market()

    def start(self) -> None:
        """Starts the game in its own thread."""
        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

    def stop(self) -> None:
        """Stops the game after finishing the current epoch."""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()
