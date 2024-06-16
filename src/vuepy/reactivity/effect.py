from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Any
from typing import Callable
from typing import List

from vuepy import log
from vuepy.reactivity import config
from vuepy.reactivity.constant import IterateKey
from vuepy.reactivity.dep import Dep
from vuepy.reactivity.dep import createDep
from vuepy.reactivity.effect_scope import EffectScope
from vuepy.reactivity.effect_scope import getCurrentScope
from vuepy.reactivity.effect_scope import recordEffectScope
from vuepy.utils.common import gen_hash_key

logger = log.getLogger()


class DepStore:
    def __init__(self):
        # self._store = weakref.WeakKeyDictionary()
        self._store: dict[str, Dep] = {}  # { target_id: Dep }

    def get_or_create(self, target) -> Dep:
        key = gen_hash_key(target)
        if key not in self._store:
            self._store[key] = createDep(key=key)
        return self._store[key]

    def get(self, target) -> Dep:
        return self._store.get(gen_hash_key(target))

    def len(self):
        return len(self._store)

    def clear(self):
        return self._store.clear()

    def __contains__(self, target) -> bool:
        return gen_hash_key(target) in self._store


class ReactiveDepStore:
    """
    dep for reactive
    {
        id(target): DepStore({
            id(key1): Dep(effect..),
            id(key2): Dep(effect..),
            ...
        }),
        ...
    }
    """

    def __init__(self):
        self._store = {}

    def get_or_create(self, target) -> DepStore:
        key = gen_hash_key(target)
        if key not in self._store:
            self._store[key] = DepStore()
        return self._store[key]

    def get(self, target) -> DepStore:
        return self._store.get(gen_hash_key(target))

    def len(self):
        return len(self._store)

    def delete(self, target):
        self._store.pop(gen_hash_key(target), None)

    def clear(self):
        self._store.clear()

    def __contains__(self, target) -> bool:
        return gen_hash_key(target) in self._store


targetMap = ReactiveDepStore()  # { target: { key: Dep } }

shouldTrack = True
activeEffect: "ReactiveEffect" | None = None
trackOpBit = 1
effectTrackDepth = 1


class IgnoreTracking:
    def __init__(self):
        self.shouldTrack = None

    def __enter__(self):
        global shouldTrack
        self.shouldTrack = shouldTrack
        shouldTrack = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        global shouldTrack
        shouldTrack = self.shouldTrack
        self.shouldTrack = False


class TrackOpTypes(enum.Enum):
    GET = 'get'
    HAS = 'has'
    ITER = 'iter'


class TriggerOpTypes(enum.Enum):
    SET = 'set'
    ADD = 'add'
    DELETE = 'delete'
    CLEAR = 'clear'
    ITER = 'iter'


EffectScheduler = Callable[..., Any]


class ReactiveEffect:
    def __init__(self, fn, scheduler: EffectScheduler = None, scope: EffectScope = None):
        self.fn = fn
        self.scheduler = scheduler
        self.scope = scope
        self.active = True
        self.parent: ReactiveEffect = None
        self.computed = None
        self.allow_recurse = False
        self.deferStop = False
        self.onStop = None
        self.onTrack = None
        self.onTrigger = None
        self.deps = []

        self.scope = getCurrentScope()
        recordEffectScope(self, self.scope)

    def __repr__(self):
        name = f"{self.fn.__name__} of {self.__class__.__name__} at {id(self)}"
        return f"{name}"

    def run(self):
        if not self.active:
            return self.fn()

        global activeEffect, trackOpBit, shouldTrack, effectTrackDepth
        parent = activeEffect
        last_should_track = shouldTrack
        while parent:
            if parent is self:
                return
            parent = parent.parent

        try:
            self.parent = activeEffect
            activeEffect = self
            shouldTrack = True

            effectTrackDepth += 1
            trackOpBit = 1 << effectTrackDepth
            # todo effectTrackDepth <= maxMarkerBits
            initDepMarkers(self.deps)
            return self.fn()
        finally:
            finalizeDepMarkers(self)

            effectTrackDepth -= 1
            trackOpBit = 1 << effectTrackDepth
            activeEffect = self.parent
            shouldTrack = last_should_track
            self.parent = None
            if self.deferStop:
                self.stop()

    def stop(self):
        if activeEffect is self:
            self.deferStop = True
        elif self.active:
            cleanupEffect(self)
            if self.onStop:
                self.onStop()
            self.active = False


# todo move to reactiveeffect
def cleanupEffect(effect: ReactiveEffect):
    for dep in effect.deps:
        dep.delete(effect)
    effect.deps = []


def track(target, track_type: TrackOpTypes, key, msg=""):
    if not (shouldTrack and activeEffect):
        return

    eventInfo = config.__DEV__ and {
        'effect': activeEffect,
        'target': target,
        'type': track_type,
        'key': key,
        'msg': msg,
    }
    if isinstance(target, list) and track_type == TrackOpTypes.ITER:
        key = IterateKey.get_key(target)
    dep = targetMap.get_or_create(target).get_or_create(key)
    trackEffects(dep, eventInfo)


def trackEffects(dep: Dep, debugger_info: DebuggerEventExtraInfo = None):
    should_track = False
    if not newTracked(dep):
        dep.n |= trackOpBit
        should_track = not wasTracked(dep)
    # else:
    #     should_track = activeEffect not in dep
    if not should_track:
        return

    dep.add(activeEffect)
    activeEffect.deps.append(dep)
    if config.__DEV__ and activeEffect.onTrack:
        activeEffect.onTrack(debugger_info)


def trigger(
        target,
        trigger_type: TriggerOpTypes,
        key=None,
        new=None,
        old=None,
        old_target=None,
        msg="",
):
    depsMap = targetMap.get(target)
    if not depsMap:
        return

    logger.debug(f"trigger %s.%s %s", target, key, msg)

    deps: List[Dep] = []
    if trigger_type in (TriggerOpTypes.CLEAR, TriggerOpTypes.ITER):
        deps.extend(depsMap.values())
    else:
        if key in depsMap:
            deps.append(depsMap.get(key))

        iter_key = IterateKey.get_key(target)

        if trigger_type == TriggerOpTypes.ADD:
            deps.append(depsMap.get(iter_key))
        elif trigger_type == TriggerOpTypes.DELETE:
            deps.append(depsMap.get(iter_key))
        elif trigger_type == TriggerOpTypes.SET:
            deps.append(depsMap.get(iter_key))

    eventInfo = config.__DEV__ and {
        'target': target,
        'type': trigger_type,
        'key': key,
        'newValue': new,
        'oldValue': old,
        'oldTarget': old_target,
        'msg': msg,
    }
    effects = []
    for dep in deps:
        if not dep:
            continue
        effects.extend(dep)

    triggerEffects(effects, eventInfo)


def triggerEffects(
        dep: Dep | List[ReactiveEffect],
        debuggerEventExtraInfo: DebuggerEventExtraInfo = None
):
    effects = dep if isinstance(dep, list) else list(dep)
    logger.debug("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    logger.debug("🚀trigger effects%s len(%s) start", id(effects), len(effects))
    for effect in list(effects):
        if effect.computed:
            trigggerEffect(effect, debuggerEventExtraInfo)

    for effect in list(effects):
        if not effect.computed:
            trigggerEffect(effect, debuggerEventExtraInfo)
    logger.debug(f"effects%s len(%s) end🚀", id(effects), len(effects))
    logger.debug("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")


def trigggerEffect(effect: ReactiveEffect, debuggerEventExtraInfo=None):
    if effect is not activeEffect or effect.allow_recurse:
        if config.__DEV__ and effect.onTrigger:
            debuggerEventExtraInfo['effect'] = effect
            effect.onTrigger(debuggerEventExtraInfo)

        if effect.scheduler:
            effect.scheduler()
        else:
            effect.run()


@dataclass
class DebuggerEventExtraInfo:
    target: Any
    type: TrackOpTypes | TriggerOpTypes
    key: Any
    newValue: Any = None
    oldValue: Any = None
    oldTarget: dict[any, any] | set[any] = None


@dataclass
class DebuggerEvent(DebuggerEventExtraInfo):
    effect: ReactiveEffect = None


@dataclass
class DebuggerOptions:
    onTrack: Callable[[DebuggerEvent], None] = None
    onTrigger: Callable[[DebuggerEvent], None] = None


@dataclass
class ReactiveEffectOptions(DebuggerOptions):
    lazy: bool = False
    scheduler: EffectScheduler = None
    scope: EffectScope = None
    allowRecurse: bool = False
    onStop: Callable[[], None] = None

    def extend(self, effect: ReactiveEffect):
        effect.onTrack = self.onTrack
        effect.onTrigger = self.onTrigger
        effect.scheduler = self.scheduler
        effect.allow_recurse = self.allowRecurse
        effect.onStop = self.onStop
        if self.scope:
            recordEffectScope(effect, self.scope)


@dataclass
class ReactiveEffectRunner:
    effect: ReactiveEffect = None

    def __call__(self):
        pass


def effect_impl(fn, options: ReactiveEffectOptions = None):
    _effect = ReactiveEffect(fn)
    if options:
        options.extend(_effect)

    if not options or not options.lazy:
        _effect.run()

    runner = ReactiveEffectRunner()
    runner.effect = _effect
    return runner


def effect(fn_or_options=None, options: ReactiveEffectOptions = None):
    is_decorator_no_arg = (fn_or_options, options) == (None, None)
    is_decorator_with_arg = isinstance(fn_or_options, ReactiveEffectOptions)
    # @effect() or @effect(options)
    if is_decorator_with_arg or is_decorator_no_arg:
        def wrap(fn):
            return effect_impl(fn, fn_or_options)

        return wrap
    # @effect or effect(fn)
    else:
        return effect_impl(fn_or_options, options)


MUTABLE_TYPES = (dict, list, set)


def _can_reactive(target) -> bool:
    return isinstance(target, MUTABLE_TYPES)


def wasTracked(dep: Dep):
    return (dep.w & trackOpBit) > 0


def newTracked(dep: Dep):
    return (dep.n & trackOpBit) > 0


def initDepMarkers(deps: List[Dep]):
    for dep in deps:
        dep.w |= trackOpBit


def finalizeDepMarkers(effect):
    # todo 可优化
    ptr = 0
    dep_len = len(effect.deps)
    for i, dep in enumerate(effect.deps):
        if wasTracked(dep) and (not newTracked(dep)):
            dep.delete(effect)
        else:
            if i != ptr:
                effect.deps[ptr] = dep
            ptr += 1

        dep.w &= ~trackOpBit
        dep.n &= ~trackOpBit

    if ptr != dep_len:
        effect.deps = effect.deps[:ptr]
