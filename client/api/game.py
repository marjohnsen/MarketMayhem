import requests
from typing import Optional, Dict, Any
from singleton import SingletonMeta


class GameAPI(metaclass=SingletonMeta):
    def __init__(self, server_address: str, game_key: str) -> None:
        self.server_address: str = server_address
        self.game_key: str = game_key
        self.player_key: Optional[str] = None

    def join_game(self, player_name: str) -> Dict[str, Any]:
        api_url = f"http://{self.server_address}/join_game"
        payload = {
            "game_key": self.game_key,
            "player_name": player_name,
        }
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        result = response.json()
        self.player_key = result.get("player_key")
        return result

    def game_status(self) -> Dict[str, Any]:
        api_url = f"http://{self.server_address}/game_status"
        payload = {
            "game_key": self.game_key,
            "player_key": self.player_key,
        }
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_latest_price(self) -> Dict[str, Any]:
        api_url = f"http://{self.server_address}/get_latest_price"
        payload = {
            "game_key": self.game_key,
            "player_key": self.player_key,
        }
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()

    def trade(self, position: int) -> Dict[str, Any]:
        api_url = f"http://{self.server_address}/trade"
        payload = {
            "game_key": self.game_key,
            "player_key": self.player_key,
            "position": position,
        }
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_scoreboard(self) -> Dict[str, Any]:
        api_url = f"http://{self.server_address}/get_scoreboard"
        payload = {"game_key": self.game_key}
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()
