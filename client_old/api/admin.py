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

        if response.status_code >= 400:
            raise requests.HTTPError(f"HTTP {response.status_code}: {response.text}")

        self.game_key = response.json().get("game_key")
        return response.json()

    def start_game(self) -> Dict[str, Any]:
        api_url = f"http://{self.server_address}/start_game"
        payload = {
            "admin_key": self.admin_key,
            "game_key": self.game_key,
        }

        response = requests.post(api_url, json=payload)

        if response.status_code >= 400:
            raise requests.HTTPError(f"HTTP {response.status_code}: {response.text}")

        return response.json()

    def stop_game(self) -> Dict[str, Any]:
        api_url = f"http://{self.server_address}/stop_game"
        payload = {
            "admin_key": self.admin_key,
            "game_key": self.game_key,
        }
        response = requests.post(api_url, json=payload)

        if response.status_code >= 400:
            raise requests.HTTPError(f"HTTP {response.status_code}: {response.text}")

        return response.json()

    def game_status(self) -> Dict[str, Any]:
        api_url = f"http://{self.server_address}/game_status"
        payload = {
            "game_key": self.game_key,
            "admin_key": self.admin_key,
        }
        response = requests.post(api_url, json=payload)

        if response.status_code >= 400:
            raise requests.HTTPError(f"HTTP {response.status_code}: {response.text}")

        return response.json()

    def list_players(self) -> Dict[str, Any]:
        api_url = f"http://{self.server_address}/list_players"
        payload = {
            "game_key": self.game_key,
            "admin_key": self.admin_key,
        }
        response = requests.post(api_url, json=payload)

        if response.status_code >= 400:
            raise requests.HTTPError(f"HTTP {response.status_code}: {response.text}")

        return response.json()


if __name__ == "__main__":
    api = AdminAPI("localhost:5000", "123")
    key = api.create_game(100, 1)
    print(f"Game Key: {key}")
    status = api.game_status()
    print(f"Game Status: {status}")
