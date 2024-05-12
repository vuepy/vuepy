import enum


class IterateKey(enum.Enum):
    DICT = 'dict'
    LIST = 'list'
    SET = 'set'

    @classmethod
    def get_key(cls, target):
        if isinstance(target, dict):
            return IterateKey.DICT
        elif isinstance(target, list):
            return IterateKey.LIST
        elif isinstance(target, set):
            return IterateKey.SET
        else:
            return None


class ErrorCodes(enum.Enum):
    WATCH_GETTER = 2
    WATCH_CALLBACK = 3
    WATCH_CLEANUP = 4
