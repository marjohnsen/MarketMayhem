import requests
from typing import Optional, Dict, Any
from api.singleton import SingletonMeta


class AdminAPI(metaclass=SingletonMeta):
    def __init__(self, server_address: str, admin_key: str) -> None:
        self.server_address: str = server_address
        self.admin_key: str = admin_key
        self.game_key: Optional[str] = None

    def create_game(self, epochs: int, timestep: int) -> Dict[str, Any]:
        api_url = f"http://{self.server_address}/create_game"
        payload = {
            "admin_key": self.admin_key,
            "epochs": epochs,
            "timestep": timestep,
        }
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        self.game_key = response.json().get("game_key")
        return response.json()

    def start_game(self) -> Dict[str, Any]:
        api_url = f"http://{self.server_address}/start_game"
        payload = {
            "admin_key": self.admin_key,
            "game_key": self.game_key,
        }
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()

    def stop_game(self) -> Dict[str, Any]:
        api_url = f"http://{self.server_address}/stop_game"
        payload = {
            "admin_key": self.admin_key,
            "game_key": self.game_key,
        }
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()

    def game_status(self) -> Dict[str, Any]:
        api_url = f"http://{self.server_address}/game_status"
        payload = {
            "game_key": self.game_key,
            "admin_key": self.admin_key,
        }
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()
