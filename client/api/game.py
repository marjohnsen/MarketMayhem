import requests
from singleton import SingletonMeta


class GameAPI(metaclass=SingletonMeta):
    def __init__(self, server_address: str, game_key: str, player_key: str):
        self.server_address = server_address
        self.game_key = game_key
        self.player_key = player_key

    def get_latest_price(self):
        api_url = f"http://{self.server_address}/get_latest_price"
        payload = {"game_key": self.game_key, "player_key": self.player_key}
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()

    def trade(self, position: int):
        api_url = f"http://{self.server_address}/trade"
        payload = {
            "game_key": self.game_key,
            "player_key": self.player_key,
            "position": position,
        }
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_scoreboard(self):
        api_url = f"http://{self.server_address}/get_scoreboard"
        payload = {"game_key": self.game_key}
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()
