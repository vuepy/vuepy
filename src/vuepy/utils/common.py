from __future__ import annotations

import dataclasses

from vuepy.log import getLogger

logger = getLogger()


def has_changed(value, old) -> bool:
    try:
        return bool(value != old)
    except Exception as e:
        logger.warn(f"Run has_changed failed, {e}")
        return True


def gen_hash_key(target):
    try:
        hash(target)
    except Exception:
        return f"id(target)={id(target)})"
    return target


class Nil:
    pass


@dataclasses.dataclass
class Record:
    def to_ns(self):
        return self.__dict__
