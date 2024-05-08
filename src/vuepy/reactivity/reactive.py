import enum
from weakref import WeakKeyDictionary

from vuepy.reactivity import DictProxy
from vuepy.reactivity import ListProxy
from vuepy.reactivity import Proxy
from vuepy.reactivity import _can_reactive
from vuepy.reactivity import is_readonly

reactiveMap = WeakKeyDictionary()  # target: any
shallowReactiveMap = WeakKeyDictionary()
readonlyMap = WeakKeyDictionary()
shallowReadonlyMap = WeakKeyDictionary()


def reactive(target) -> "Proxy":
    if is_readonly(target):
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


TARGET_PROXY_MAP = {
    TargetType.COMMON: Proxy,
    TargetType.DICT: DictProxy,
    TargetType.LIST: ListProxy,
}


def createReactiveObject(target, is_readonly: bool, proxyMap: WeakKeyDictionary) -> Proxy:
    if not _can_reactive(target):
        # todo __DEV__ log
        return target

    # target is already a Proxy, return it
    if isinstance(target, Proxy):
        return target

    # target already has corresponding Proxy
    existing_proxy = proxyMap.get(target)
    if existing_proxy:
        return existing_proxy

    # only specific value types can be observed
    target_type = getTargetType(target)
    if target_type == TargetType.INVALID:
        return target

    _proxy = TARGET_PROXY_MAP[target_type](target)
    proxyMap[target] = _proxy
    return _proxy


def toReactive(value):
    return reactive(value) if _can_reactive(value) else value


def to_raw(proxy):
    pass


def is_proxy(value) -> bool:
    pass


def is_reactive(value) -> bool:
    pass


def shallow_reactive(target):
    pass


def shallow_readonly(target):
    pass


def isShallow(value) -> bool:
    return False