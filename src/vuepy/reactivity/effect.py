import enum
from typing import List

shouldTrack = True

activeEffect = None


class TrackOpTypes(enum.Enum):
    GET = 'get'
    HAS = 'has'
    ITER = 'iter'


class TriggerOpTypes(enum.Enum):
    SET = 'set'
    ADD = 'add'
    DELETE = 'delete'
    CLEAR = 'clear'


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


def track(target, track_type: TrackOpTypes, key):
    pass


def trigger(
        target,
        trigger_type: TriggerOpTypes,
        key=None,
        new=None,
        old=None,
        old_target=None
):
    pass


def trackEffects():
    pass


def triggerEffects():
    pass


MUTABLE_TYPES = (dict, list, set)


def _can_reactive(target) -> bool:
    return isinstance(target, MUTABLE_TYPES)