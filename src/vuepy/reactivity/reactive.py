from __future__ import annotations

import enum
from weakref import WeakKeyDictionary

from vuepy.reactivity.constant import IterateKey
from vuepy.reactivity.effect import TrackOpTypes
from vuepy.reactivity.effect import TriggerOpTypes
from vuepy.reactivity.effect import _can_reactive
from vuepy.reactivity.effect import targetMap
from vuepy.reactivity.effect import track
from vuepy.reactivity.effect import trigger
from vuepy.utils.common import Nil
from vuepy.utils.common import gen_hash_key
from vuepy.utils.common import has_changed


class ReactiveFlags(enum.Enum):
    SKIP = '_v_skip_'
    IS_REACTIVE = '_v_isReactive_'
    IS_READONLY = '_v_isReadonly_'
    IS_SHALLOW = '_v_isShallow_'
    RAW = '_v_raw_'


class ProxyStore:
    """
    proxy for target
    """

    def __init__(self):
        # { id(target): Proxy }
        self._store: dict[int, "ReactiveProxy"] = {}  # weakref.WeakValueDictionary()

    def get(self, target):
        return self._store.get(gen_hash_key(target))

    def set(self, target, proxy):
        self._store[gen_hash_key(target)] = proxy

    def delete(self, target):
        self._store.pop(gen_hash_key(target), None)

    def clear(self):
        self._store.clear()

    def len(self):
        return len(self._store)

    def __contains__(self, target):
        return gen_hash_key(target) in self._store


reactiveMap = ProxyStore()
shallowReactiveMap = WeakKeyDictionary()
readonlyMap = WeakKeyDictionary()
shallowReadonlyMap = WeakKeyDictionary()


def reactive(target) -> "ReactiveProxy" | "DictProxy" | "ListProxy":
    if isReadonly(target):
        return target

    return createReactiveObject(
        target,
        False,
        reactiveMap,
    )


class TargetType(enum.Enum):
    INVALID = 0
    COMMON = 1
    LIST = 2
    DICT = 3
    COLLECTION = 4


def getTargetType(value):
    # todo add class to common
    if isinstance(value, (list,)):
        return TargetType.LIST
    elif isinstance(value, (dict,)):
        return TargetType.DICT
    else:
        return TargetType.INVALID


class ReactiveProxy:
    ATTR_TARGET = '_vp_target_'
    ATTR_TRACK_TARGET = '_vp_track_target_'
    ATTR_SHALLOW = '_vp_shallow_'

    PROXY_ATTRS = (
        ATTR_TARGET,
        ATTR_TRACK_TARGET,
        ATTR_SHALLOW,
    )
    DICT_ATTRS = ('__class__',)

    def __init__(self, target, track_target, shallow: bool):
        self._vp_target_ = target
        self._vp_shallow_ = track_target
        self._vp_track_target_ = shallow


class DictProxy(ReactiveProxy):
    def __init__(self, target: dict, shallow: bool = False):
        super().__setattr__(ReactiveProxy.ATTR_TARGET, target)
        super().__setattr__(ReactiveProxy.ATTR_TRACK_TARGET, target)
        super().__setattr__(ReactiveProxy.ATTR_SHALLOW, shallow)

    def __delete__(self, instance):
        track_target = self._vp_track_target_
        print(f"delete {track_target}")
        targetMap.delete(track_target)
        reactiveMap.delete(track_target)

    def __getattribute__(self, name):
        if name in ReactiveProxy.PROXY_ATTRS:
            return super().__getattribute__(name)

        target = super().__getattribute__(ReactiveProxy.ATTR_TARGET)
        if name in ReactiveProxy.DICT_ATTRS:
            return getattr(target, name)

        if name not in target:
            return super().__getattribute__(name)

        track(self._vp_track_target_, TrackOpTypes.GET, name, "__getattribute__")
        res = target[name]
        return toReactive(res)

    def __setattr__(self, name, value):
        if name == ReactiveProxy.ATTR_TARGET:
            raise KeyError(f"can't set {name}")

        target = self._vp_target_
        old_value = target.get(name, Nil)
        if not self._vp_shallow_:
            if not isShallow(value):
                old_value = to_raw(old_value)
                value = to_raw(value)

            # # reactive unpack value
            # if is_ref(old_value) and not is_ref(value):
            #     old_value.value = value
            #     return

        target[name] = value
        if old_value is Nil:
            trigger(self._vp_track_target_, TriggerOpTypes.ADD, name, value, Nil, msg="__setattr__ by add")
        elif has_changed(value, old_value):
            trigger(self._vp_track_target_, TriggerOpTypes.SET, name, value, old_value, msg="__setattr__ by set")
            targetMap.delete(old_value)
            reactiveMap.delete(old_value)

    def __delattr__(self, name):
        target = self._vp_target_
        old_value = target.get(name, Nil)
        if old_value is Nil:
            return
        del target[name]
        trigger(self._vp_track_target_, TriggerOpTypes.DELETE, name, Nil, old_value, msg="delattr")

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __delitem__(self, key):
        self.__delattr__(key)

    def __iter__(self):
        track(self._vp_track_target_, TrackOpTypes.ITER, IterateKey.DICT, msg="__iter__")
        return iter(self._vp_target_)

    def __contains__(self, key):
        track(self._vp_track_target_, TrackOpTypes.HAS, key, msg='__contains__')
        return key in self._vp_target_

    def __len__(self):
        track(self._vp_track_target_, TrackOpTypes.ITER, IterateKey.DICT, msg="__len__")
        return len(self._vp_target_)

    def __repr__(self):
        track(self._vp_track_target_, TrackOpTypes.ITER, IterateKey.DICT, msg="__repr__")
        return repr(self._vp_target_)

    def __str__(self):
        track(self._vp_track_target_, TrackOpTypes.ITER, IterateKey.DICT, msg="__str__")
        return str(self._vp_target_)

    def __format__(self, format_spec):
        track(self._vp_track_target_, TrackOpTypes.ITER, IterateKey.DICT, msg="__format__")
        return self._vp_target_.__format__(format_spec)

    def clear(self):
        ret = self._vp_target_.clear()
        for key in list(self._vp_target_.keys()):
            trigger(self._vp_track_target_, TriggerOpTypes.CLEAR, key, Nil, msg="clear")
        return ret

    def copy(self):
        track(self._vp_track_target_, TrackOpTypes.ITER, IterateKey.DICT, msg="copy")
        return self._vp_target_.copy()

    def get(self, key, default=None):
        track(self._vp_track_target_, TrackOpTypes.GET, key, msg="get")
        res = self._vp_target_.get(key, default)
        return toReactive(res)

    def keys(self):
        track(self._vp_track_target_, TrackOpTypes.ITER, IterateKey.DICT, msg="keys")
        return self._vp_target_.keys()

    def values(self):
        track(self._vp_track_target_, TrackOpTypes.ITER, IterateKey.DICT, msg="values")
        return (toReactive(value) for value in self._vp_target_.values())

    def items(self):
        track(self._vp_track_target_, TrackOpTypes.ITER, IterateKey.DICT, msg="items")
        return ((k, toReactive(v)) for k, v in self._vp_target_.items())

    def pop(self, key, default=None):
        ret = self._vp_target_.pop(key, default)
        trigger(self._vp_track_target_, TriggerOpTypes.DELETE, key, None, msg="pop")
        return ret

    def popitem(self):
        key, value = self._vp_target_.popitem()
        trigger(self._vp_track_target_, TriggerOpTypes.DELETE, key, None, msg="popitem")
        return key, value

    def setdefault(self, key, default=None):
        if key in self._vp_target_:
            return
        ret = self.__setattr__(key, default)
        return ret

    def update(self, other):
        for key, value in other.items():
            self.__setattr__(key, value)


class ListProxy(ReactiveProxy):
    def __init__(self, target: list, shallow: bool = False):
        super().__setattr__(ReactiveProxy.ATTR_TARGET, target)
        super().__setattr__(ReactiveProxy.ATTR_TRACK_TARGET, target)
        super().__setattr__(ReactiveProxy.ATTR_SHALLOW, shallow)

    def __getitem__(self, index):
        target = self._vp_target_
        index = index if index >= 0 else len(target) + index
        res = target[index]
        track(self._vp_track_target_, TrackOpTypes.ITER, index, "list.__getitem__")
        return toReactive(res)

    def __setitem__(self, index, value):
        target = self._vp_target_
        old_value = target[index] if index < len(target) else Nil

        target[index] = value
        if has_changed(value, old_value):
            trigger(self._vp_track_target_, TriggerOpTypes.SET, index, value, old_value,
                    msg="__setitem__ by set")
            targetMap.delete(old_value)
            reactiveMap.delete(old_value)

    def __delitem__(self, index):
        target = self._vp_target_
        old_value = target[index] if index < len(target) else Nil
        if old_value is Nil:
            return
        del target[index]
        trigger(self._vp_track_target_, TriggerOpTypes.ITER, IterateKey.LIST, msg="__delitem__")

    def __iter__(self):
        track(self._vp_track_target_, TrackOpTypes.ITER, IterateKey.LIST, msg="__iter__")
        return iter(toReactive(item) for item in self._vp_target_)

    def __contains__(self, item):
        track(self._vp_track_target_, TrackOpTypes.ITER, item, msg='__contains__')
        return item in self._vp_target_

    def __len__(self):
        track(self._vp_track_target_, TrackOpTypes.ITER, IterateKey.LIST, msg="__len__")
        return len(self._vp_target_)

    def __repr__(self):
        track(self._vp_track_target_, TrackOpTypes.ITER, IterateKey.LIST, msg="__repr__")
        return f"{self.__class__.__name__}: {repr(self._vp_target_)}"

    def __str__(self):
        track(self._vp_track_target_, TrackOpTypes.ITER, IterateKey.LIST, msg="__str__")
        return f"{self.__class__.__name__}: {str(self._vp_target_)}"

    def append(self, item):
        ret = self._vp_target_.append(item)
        trigger(self._vp_track_target_, TriggerOpTypes.ADD, len(self._vp_target_), item,
                msg="append")
        return ret

    def clear(self):
        ret = self._vp_target_.clear()
        trigger(self._vp_track_target_, TriggerOpTypes.CLEAR, None, msg="clear")
        return ret

    def copy(self):
        track(self._vp_track_target_, TrackOpTypes.ITER, IterateKey.LIST, msg="copy")
        return self._vp_target_.copy()

    def count(self, item):
        track(self._vp_track_target_, TrackOpTypes.ITER, IterateKey.LIST, msg="count")
        return self._vp_target_.count(item)

    def extend(self, iterable):
        self._vp_target_.extend(iterable)
        trigger(self._vp_track_target_, TriggerOpTypes.ADD, IterateKey.LIST, msg="extend")

    def index(self, item, start=0, end=None):
        track(self._vp_track_target_, TrackOpTypes.ITER, item, msg="index")
        return self._vp_target_.index(item, start, end)

    def insert(self, index, item):
        ret = self._vp_target_.insert(index, item)
        trigger(self._vp_track_target_, TriggerOpTypes.ADD, IterateKey.LIST, msg="insert")
        return ret

    def pop(self, index=-1):
        ret = self._vp_target_.pop(index)
        trigger(self._vp_track_target_, TriggerOpTypes.DELETE, IterateKey.LIST, msg="pop")
        return ret

    def remove(self, item):
        index = self._vp_target_.index(item)
        return self.__delitem__(index)

    def reverse(self):
        ret = self._vp_target_.reverse()
        trigger(self._vp_track_target_, TriggerOpTypes.ITER, IterateKey.LIST, msg="reverse")
        return ret

    def sort(self, key=None, reverse=False):
        ret = self._vp_target_.sort(key=key, reverse=reverse)
        trigger(self._vp_track_target_, TriggerOpTypes.ITER, IterateKey.LIST, msg="sort")
        return ret


TARGET_PROXY_MAP = {
    TargetType.COMMON: ReactiveProxy,
    TargetType.DICT: DictProxy,
    TargetType.LIST: ListProxy,
}


def createReactiveObject(target, is_readonly: bool, proxyMap: ProxyStore) -> ReactiveProxy:
    if not _can_reactive(target):
        # todo __DEV__ log
        return target

    # target is already a Proxy, return it
    if isinstance(target, ReactiveProxy):
        return target

    # target already has corresponding Proxy
    # can't use the `if exist_proxy` method because `if` will call the __len__ method to track
    if target in proxyMap:
        return proxyMap.get(target)

    # only specific value types can be observed
    target_type = getTargetType(target)
    if target_type == TargetType.INVALID:
        return target

    _proxy = TARGET_PROXY_MAP[target_type](target)
    proxyMap.set(target, _proxy)
    return _proxy


def toReactive(value):
    return reactive(value) if _can_reactive(value) else value


def to_raw(proxy):
    if isinstance(proxy, ReactiveProxy):
        return proxy._vp_target_

    return proxy


toRaw = to_raw


def is_reactive(value) -> bool:
    return isinstance(value, ReactiveProxy)


isReactive = is_reactive


def shallow_reactive(target):
    pass


def shallow_readonly(target):
    pass


def isShallow(value) -> bool:
    return False


def isReadonly(value) -> bool:
    return False


def isProxy(value):
    return is_reactive(value) or isReadonly(value)
