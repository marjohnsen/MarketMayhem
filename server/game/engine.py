import threading
import time
from typing import List, Literal, Optional

from game.exchange import Exchange
from game.market import Market


class GameEngine:
    """Orchestrates the game loop."""

    def __init__(self, epochs: int, timestep: int) -> None:
        self.timestep: int = timestep
        self.status: Literal["waiting", "running", "done", "stopped"] = "waiting"
        self.thread: Optional[threading.Thread] = None

        market = Market(epochs)
        self.exchange: Exchange = Exchange(market)

    def run(self) -> None:
        self.status = "running"
        while self.exchange.market.epoch < self.exchange.market.epochs and self.status == "running":
            time.sleep(((self.timestep - 0.1) - (time.time() % self.timestep)) % self.timestep)
            self.exchange.update_market()
        self.status = "done"

    def start(self, player_keys: List[str]) -> None:
        if self.status != "waiting":
            raise RuntimeError(
                f"The game status must be 'waiting' to start. Current status: {self.status}"
            )

        for key in player_keys:
            self.exchange.add_player_account(key)

        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

    def stop(self) -> None:
        self.status = "stopped"
        if self.thread and self.thread.is_alive():
            self.thread.join()
