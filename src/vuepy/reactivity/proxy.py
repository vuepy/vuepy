
class Proxy:
    def __init__(self, target):
        self._vp_target = target


class DictProxy(Proxy):
    def __init__(self, target: dict):
        super().__init__(target)

    def __getattribute__(self, name):
        target = super().__getattribute__('_vp_target')

        if name in ['target', '__class__', '__repr__', '__str__']:
            return super().__getattribute__(name)

        if name in target:
            return target[name]
        else:
            return getattr(target, name)

    def __setattr__(self, name, value):
        if name == 'target':
            super().__setattr__(name, value)
        else:
            self._vp_target[name] = value

    def __delattr__(self, name):
        if name in self._vp_target:
            del self._vp_target[name]
        else:
            super().__delattr__(name)

    def __getitem__(self, key):
        return self._vp_target[key]

    def __setitem__(self, key, value):
        self._vp_target[key] = value

    def __delitem__(self, key):
        del self._vp_target[key]

    def __iter__(self):
        return iter(self._vp_target)

    def __contains__(self, key):
        return key in self._vp_target

    def __len__(self):
        return len(self._vp_target)

    def __repr__(self):
        return repr(self._vp_target)

    def clear(self):
        return self._vp_target.clear()

    def copy(self):
        return self._vp_target.copy()

    @classmethod
    def fromkeys(cls, iterable, value=None):
        return dict.fromkeys(iterable, value)

    def get(self, key, default=None):
        return self._vp_target.get(key, default)

    def items(self):
        return self._vp_target.items()

    def keys(self):
        return self._vp_target.keys()

    def pop(self, key, default=None):
        return self._vp_target.pop(key, default)

    def popitem(self):
        return self._vp_target.popitem()

    def setdefault(self, key, default=None):
        return self._vp_target.setdefault(key, default)

    def update(self, other):
        return self._vp_target.update(other)

    def values(self):
        return self._vp_target.values()


class ListProxy(Proxy):
    def __init__(self, target: dict):
        super().__init__(target)
