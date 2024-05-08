

def has_changed(value, old) -> bool:
    try:
        return value == old
    except:
        return True


class Nil:
    pass
