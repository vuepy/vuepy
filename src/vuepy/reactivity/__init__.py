import enum
from typing import List
from weakref import WeakKeyDictionary
from vuepy.reactivity import Proxy

from vuepy.reactivity import effect
from vuepy.reactivity.effect import ReactiveEffect
from vuepy.reactivity.proxy import DictProxy
from vuepy.reactivity.proxy import ListProxy
from vuepy.reactivity.proxy import Proxy

MUTABLE_TYPES = (dict, list, set)
reactiveMap = WeakKeyDictionary()  # target: any
shallowReactiveMap = WeakKeyDictionary()
readonlyMap = WeakKeyDictionary()
shallowReadonlyMap = WeakKeyDictionary()


def is_ref(r) -> bool:
    pass


def unref(ref):
    return ref.value if is_ref(ref) else ref


def to_ref(value):
    pass


def to_value(source):
    pass


def to_refs(obj):
    pass


def is_proxy(value) -> bool:
    pass


def is_reactive(value) -> bool:
    pass


def is_readonly(value) -> bool:
    return False


def shallow_ref(value) -> "ShallowRef":
    pass


def trigger_ref(ref: "ShallowRef"):
    pass


def custom_ref(factory: "CustomRefFactory") -> "Ref":
    pass


class ShallowRef:
    pass


class CustomRefFactory:
    def __init__(self, track, trigger):
        self.track = track
        self.trigger = trigger

    def get(self):
        pass

    def set(self, value):
        pass


class Ref:
    pass


def shallow_reactive(target):
    pass


def shallow_readonly(target):
    pass


def to_raw(proxy):
    pass


def mark_raw(value):
    pass


def effect_scope(detached: bool) -> "EffectScope":
    pass


def get_current_scope() -> "EffectScope":
    pass


def on_scope_dispose():
    pass


def ref(value) -> Ref:
    return _create_ref(value, False)


def _create_ref(raw_value, shallow: bool):
    if is_ref(raw_value):
        return raw_value

    return RefImpl(raw_value, shallow)


class RefImpl:
    def __init__(self, value, is_shallow):
        self._is_shallow = is_shallow
        self._raw_value = value if is_shallow else to_raw(value)
        self._value = value if is_shallow else _to_reactive(value)

    @property
    def value(self):
        trackRefValue(self)
        return self._value

    @value.setter
    def value(self, new_val):
        use_direct_value = self._is_shallow or isShallow(new_val) or is_readonly(new_val)
        new_val = new_val if use_direct_value else to_raw(new_val)
        if new_val != self._raw_value:
            self._raw_value = new_val
            self._value = new_val if use_direct_value else toReactive(new_val)
            triggerRefValue(self, new_val)


def toReactive(value):
    return reactive(value) if _can_reactive(value) else value


class Dep(set):
    def __init__(self, *args, **kwargs):
        self.w = kwargs.pop('w', 0)
        self.n = kwargs.pop('n', 0)
        super().__init__(*args, **kwargs)


def createDep(effects: ReactiveEffect = None) -> Dep:
    return Dep(effects or "")


def trackRefValue(ref):
    if effect.shouldTrack and effect.activeEffect:
        ref = to_raw(ref)
        # __DEV__
        dep = getattr(ref, 'dep', None)
        if dep is None:
            dep = createDep()
            ref.dep = dep

        trackEffects(ref.dep)


def computed(getter, debugger_options) -> Ref:
    pass


def _can_reactive(target) -> bool:
    return isinstance(target, MUTABLE_TYPES)


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


def createReactiveObject(target, is_readonly:bool, proxyMap: WeakKeyDictionary) -> "Proxy":
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


def readonly(target):
    pass


def watch_effect(effect, options: "WatchEffectOptions") -> "StopHandle":
    pass


class WatchEffectOptions:
    def __init__(self):
        self.flush = 'pre'  # pre, post, sync

    def on_track(self, event: "DebuggerEvent"):
        pass

    def on_trigger(self, event: "DebuggerEvent"):
        pass


class WatchPostEffect(WatchEffectOptions):
    def __init__(self):
        super().__init__()
        self.flush = 'post'


class WatchSyncEffect(WatchEffectOptions):
    def __init__(self):
        super().__init__()
        self.flush = 'sync'


class DebuggerEvent:
    pass


class StopHandle:
    pass


WatchSource = Ref  # ref, getter


class WatchCallback:
    def __init__(self, value, old_value, on_cleanup):
        pass


class WatchOptions(WatchEffectOptions):
    def __init__(self):
        super().__init__()
        self.immediate = False
        self.deep = False
        self.once = False


def watch(
        source: WatchSource | List[WatchSource],
        callback: WatchCallback,
        options: WatchOptions
) -> StopHandle:
    pass


