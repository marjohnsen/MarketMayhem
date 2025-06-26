import pkgutil
import importlib

__all__ = []
for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f"{__name__}.{module_name}")
    for attr_name in dir(module):
        if attr_name.endswith("Menu"):
            globals()[attr_name] = getattr(module, attr_name)
            __all__.append(attr_name)
