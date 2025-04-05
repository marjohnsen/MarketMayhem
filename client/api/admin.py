import requests
from api.singleton import SingletonMeta


class AdminAPI(metaclass=SingletonMeta):
    def __init__(self, server_address: str, admin_key: str):
        self.server_address = server_address
        self.admin_key = admin_key
        self.game_key = None

    def create_game(self):
        api_url = f"http://{self.server_address}/create_game"
        response = requests.post(api_url, json={"admin_key": self.admin_key})
        response.raise_for_status()
        self.game_key = response.json().get("game_key")
        return response.json()

    def start_game(self, game_key: str, epochs: int, timestep: float):
        api_url = f"http://{self.server_address}/start_game"
        payload = {
            "admin_key": self.admin_key,
            "game_key": game_key,
            "epochs": epochs,
            "timestep": timestep,
        }
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()

    def change_player_state(self, game_key: str, player_name: str, new_state: str):
        api_url = f"http://{self.server_address}/change_player_state"
        payload = {
            "admin_key": self.admin_key,
            "game_key": game_key,
            "player_name": player_name,
            "new_state": new_state,
        }
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()
