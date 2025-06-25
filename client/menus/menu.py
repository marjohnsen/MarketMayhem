from abc import ABC, abstractmethod


class Menu(ABC):
    @abstractmethod
    def draw(self, canvas): ...

    @abstractmethod
    def route(self, key) -> "Menu|None": ...
