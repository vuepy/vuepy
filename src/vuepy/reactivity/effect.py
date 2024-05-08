from typing import List

shouldTrack = True

activeEffect = None


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



