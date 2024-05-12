from __future__ import annotations


class Nil:
    pass


def has_changed(value, old) -> bool:
    try:
        return value != old
    except:
        return True


def gen_hash_key(target):
    try:
        hash(target)
    except Exception:
        return f"id(target)={id(target)})"
    return target
