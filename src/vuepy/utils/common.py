# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

import dataclasses
from typing import Iterable

from vuepy.log import getLogger

logger = getLogger()


def has_changed(value, old) -> bool:
    try:
        ret = (value != old)
        if isinstance(ret, Iterable):
            return any(ret)
        else:
            logger.warning(f"{value}, {old}, ref={ret}")
            return bool(ret)
    except ValueError as e:
        try:
            return ret.any()
        except Exception as e:
            logger.warning(f"Run has_changed failed, {e}")
            return True
    except Exception as e:
        logger.warning(f"Run has_changed failed, {e}")
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
