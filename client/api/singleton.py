class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls in cls._instances:
            if args or kwargs:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        else:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]
