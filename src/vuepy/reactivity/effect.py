from __future__ import annotations
import enum
import weakref
from collections import defaultdict
from typing import Any
from typing import List
from typing import Type

from vuepy.reactivity import createDep
from vuepy.reactivity.dep import Dep
from vuepy.reactivity.dep import newTracked
from vuepy.reactivity.dep import wasTracked


class DepStore:
    def __init__(self):
        self._store = defaultdict(createDep)

    def get(self, target):
        return self._store[target]

    def __contains__(self, target):
        return target in self._store


DEP_STORE = DepStore()

KeyToDepMap = Type[dict[Any, Dep]]
# obj: KeyToDepMap
targetMap = weakref.WeakKeyDictionary()

shouldTrack = True
activeEffect: "ReactiveEffect" | None = None
trackOpBit = 1



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


def recordEffectScope(effect: "ReactiveEffect", scope: "EffectScope" = None):
    if scope and scope.active:
        scope.effects.append(effect)


class EffectScope:
    def __init__(self):
        self.active = True
        self.effects: List["ReactiveEffect"] = []

    def run(self, fn):
        pass

    def stop(self):
        pass


class EffectScheduler :
    pass


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

        recordEffectScope(self, self.scope)

    def run(self):
        pass

    def stop(self):
        pass


def track(target, track_type: TrackOpTypes, key):
    if not (shouldTrack and activeEffect):
        return

    # todo weakref defaultdict
    depsMap = targetMap.get(target, None)
    if depsMap is None:
        depsMap = {}
        targetMap[target] = depsMap

    dep = depsMap.get(key, None)
    if dep is None:
        dep = createDep()
        depsMap[key] = dep
    trackEffects(dep)


def trackEffects(dep: Dep, debuggerEventExtraInfo=None):
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


def trigger(
        target,
        trigger_type: TriggerOpTypes,
        key=None,
        new=None,
        old=None,
        old_target=None
):
    pass

def triggerEffects():
    pass


MUTABLE_TYPES = (dict, list, set)


def _can_reactive(target) -> bool:
    return isinstance(target, MUTABLE_TYPES)