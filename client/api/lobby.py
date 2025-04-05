import requests
from singleton import SingletonMeta


class LobbyAPI(metaclass=SingletonMeta):
    def __init__(self, server_address: str):
        self.server_address = server_address

    def join_game(self, game_key: str, player_name: str):
        api_url = f"http://{self.server_address}/join_game"
        payload = {"game_key": game_key, "player_name": player_name}
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_game_status(self, game_key: str, player_key: str):
        api_url = f"http://{self.server_address}/get_game_status"
        payload = {"game_key": game_key, "player_key": player_key}
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()
