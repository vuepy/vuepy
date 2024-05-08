from vuepy.reactivity import _can_reactive
from vuepy.reactivity import reactive
from vuepy.reactivity import to_raw
from vuepy.reactivity.effect import TrackOpTypes
from vuepy.reactivity.effect import TriggerOpTypes

from vuepy.reactivity.effect import track
from vuepy.reactivity.effect import trigger
from vuepy.reactivity.reactive import isShallow
from vuepy.reactivity.ref import is_ref
from vuepy.utils.general import Nil
from vuepy.utils.general import has_changed


class Proxy:
    def __init__(self, target, shallow: bool = False):
        self.__vp_target = target
        self.__vp_shallow = shallow


ATTR_TARGET = '__vp_target'
ATTR_SHALLOW = '__vp_shadow'
PROXY_ATTRS = (ATTR_TARGET, ATTR_SHALLOW)


class DictProxy(Proxy):
    def __init__(self, target: dict, shallow: bool = False):
        super().__init__(target, shallow)

    def __getattribute__(self, name):
        if name in PROXY_ATTRS:
            return super().__getattribute__(name)

        target = super().__getattribute__(ATTR_TARGET)

        if name not in target:
            raise KeyError(name)

        # todo track self ?
        track(target, TrackOpTypes.GET, name)
        res = target[name]
        if _can_reactive(res):
            return reactive(res)
        else:
            return res

    def __setattr__(self, name, value):
        if name == ATTR_TARGET:
            raise KeyError(f"can't set {ATTR_TARGET}")

        target = self.__vp_target
        old_value = target.get(name, Nil)
        if not self.__vp_shallow:
            if not isShallow(value):
                old_value = to_raw(old_value)
                value = to_raw(value)

            # # reactive中不自动解 value
            # if is_ref(old_value) and not is_ref(value):
            #     old_value.value = value
            #     return

        had_name = name in target
        target[name] = value
        if not had_name:
            trigger(self.__vp_target, TriggerOpTypes.ADD, name, value)
        elif has_changed(value, old_value):
            trigger(self.__vp_target, TriggerOpTypes.SET, name, value, old_value)

    def __delattr__(self, name):
        if name in self.__vp_target:
            trigger(self.__vp_target, TriggerOpTypes.SET, name, None)
            del self.__vp_target[name]
        else:
            super().__delattr__(name)

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __setitem__(self, key, value):
        trigger(self.__vp_target, TriggerOpTypes.SET, key, value)
        self.__vp_target[key] = value

    def __delitem__(self, key):
        trigger(self.__vp_target, TriggerOpTypes.SET, key, None)
        del self.__vp_target[key]

    def __iter__(self):
        return iter(self.__vp_target)

    def __contains__(self, key):
        track(self.__vp_target, TrackOpTypes.GET, key)
        return key in self.__vp_target

    def __len__(self):
        return len(self.__vp_target)

    def __repr__(self):
        return repr(self.__vp_target)

    def __str__(self):
        pass

    def __format__(self, format_spec):
        pass

    def clear(self):
        for key in list(self.__vp_target.keys()):
            trigger(self.__vp_target, TriggerOpTypes.SET, key, None)
        return self.__vp_target.clear()

    def copy(self):
        return self.__vp_target.copy()

    @classmethod
    def fromkeys(cls, iterable, value=None):
        return dict.fromkeys(iterable, value)

    def get(self, key, default=None):
        track(self.__vp_target, TrackOpTypes.GET, key)
        return self.__vp_target.get(key, default)

    def items(self):
        return self.__vp_target.items()

    def keys(self):
        return self.__vp_target.keys()

    def pop(self, key, default=None):
        trigger(self.__vp_target, TriggerOpTypes.SET, key, None)
        return self.__vp_target.pop(key, default)

    def popitem(self):
        key, value = self.__vp_target.popitem()
        trigger(self.__vp_target, TriggerOpTypes.SET, key, None)
        return key, value

    def setdefault(self, key, default=None):
        if key not in self.__vp_target:
            trigger(self.__vp_target, TriggerOpTypes.SET, key, default)
        return self.__vp_target.setdefault(key, default)

    def update(self, other):
        for key, value in other.items():
            trigger(self.__vp_target, TriggerOpTypes.SET, key, value)
        return self.__vp_target.update(other)

    def values(self):
        return self.__vp_target.values()


class ListProxy(Proxy):
    def __init__(self, target: list):
        super().__init__(target)

    def __getattribute__(self, name):
        target = super().__getattribute__('__vp_target')

        if name in ['target', '__class__', '__repr__', '__str__']:
            return super().__getattribute__(name)

        return getattr(target, name)

    def __getitem__(self, index):
        track(self.__vp_target, TrackOpTypes.GET.value, index)
        return self.__vp_target[index]

    def __setitem__(self, index, value):
        trigger(self.__vp_target, TriggerOpTypes.SET.value, index, value)
        self.__vp_target[index] = value

    def __delitem__(self, index):
        trigger(self.__vp_target, TriggerOpTypes.DELETE.value, index)
        del self.__vp_target[index]

    def __iter__(self):
        track(self.__vp_target, TrackOpTypes.ITER.value, None)
        return iter(self.__vp_target)

    def __contains__(self, item):
        track(self.__vp_target, TrackOpTypes.HAS.value, None)
        return item in self.__vp_target

    def __len__(self):
        return len(self.__vp_target)

    def append(self, item):
        trigger(self.__vp_target, TriggerOpTypes.ADD.value, len(self.__vp_target), item)
        self.__vp_target.append(item)

    def clear(self):
        trigger(self.__vp_target, TriggerOpTypes.CLEAR.value, None)
        self.__vp_target.clear()

    def copy(self):
        return self.__vp_target.copy()

    def count(self, item):
        return self.__vp_target.count(item)

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def index(self, item, start=0, end=None):
        return self.__vp_target.index(item, start, end if end is not None else len(self.__vp_target))

    def insert(self, index, item):
        trigger(self.__vp_target, TriggerOpTypes.ADD.value, index, item)
        self.__vp_target.insert(index, item)

    def pop(self, index=-1):
        trigger(self.__vp_target, TriggerOpTypes.DELETE.value, index)
        return self.__vp_target.pop(index)

    def remove(self, item):
        index = self.__vp_target.index(item)
        self.__delitem__(index)

    def reverse(self):
        self.__vp_target.reverse()

    def sort(self, key=None, reverse=False):
        self.__vp_target.sort(key=key, reverse=reverse)

