from abc import ABC, abstractmethod


class MenuInterface(ABC):
    @abstractmethod
    def draw(self, canvas): ...

    @abstractmethod
    def route(self, key) -> "Menu|None": ...
