import requests
from singleton import SingletonMeta


class LobbyAPI(metaclass=SingletonMeta):
    def __init__(self, server_address: str):
        self.server_address = server_address

    def join_session(self, session_key: str, player_name: str):
        api_url = f"http://{self.server_address}/join_session"
        payload = {"session_key": session_key, "player_name": player_name}
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_session_status(self, session_key: str, player_key: str):
        api_url = f"http://{self.server_address}/get_session_status"
        payload = {"session_key": session_key, "player_key": player_key}
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()
