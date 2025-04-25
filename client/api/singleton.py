from typing import Any, Dict, Type


class SingletonMeta(type):
    _instances: Dict[Type, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls in cls._instances:
            if args or kwargs:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        else:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]

    def delete(cls) -> None:
        cls._instances.pop(cls, None)
