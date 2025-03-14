import os
import inspect
import importlib.util
from game.simulators.interface import MarketSimulatorInterface


class SingletonCatalogMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

    def __getitem__(cls, key):
        return cls().__getitem__(key)

    def __iter__(cls):
        return cls().__iter__()

    def __len__(cls):
        return cls().__len__()

    def __repr__(cls):
        return cls().__repr__()


class SimulatorCatalog(metaclass=SingletonCatalogMeta):
    def __init__(self):
        self._classes = {}
        folder = os.path.abspath(os.path.dirname(__file__))
        for fname in os.listdir(folder):
            if fname.endswith(".py") and not fname.startswith("__"):
                module_path = os.path.join(folder, fname)
                spec = importlib.util.spec_from_file_location(fname[:-3], module_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for name, cls in inspect.getmembers(module, inspect.isclass):
                        if cls.__module__ == module.__name__ and issubclass(cls, MarketSimulatorInterface):
                            self._classes[name] = cls

    def __getitem__(self, key: str):
        return self._classes[key]

    def __iter__(self):
        return iter(self._classes)

    def __len__(self):
        return len(self._classes)

    def __repr__(self):
        return repr(list(self._classes.keys()))


if __name__ == "__main__":
    print("Available simulators:", list(SimulatorCatalog))
    print("Found simulator:", SimulatorCatalog["GaussianMarketSimulator"])
