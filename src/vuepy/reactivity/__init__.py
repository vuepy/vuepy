from typing import List

from vuepy.reactivity import effect
from vuepy.reactivity.dep import createDep
from vuepy.reactivity.effect import ReactiveEffect
from vuepy.reactivity.effect import _can_reactive
from vuepy.reactivity.proxy import DictProxy
from vuepy.reactivity.proxy import ListProxy
from vuepy.reactivity.proxy import Proxy
from vuepy.reactivity.reactive import reactive
from vuepy.reactivity.reactive import reactiveMap
from vuepy.reactivity.reactive import to_raw


def is_readonly(value) -> bool:
    return False


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


def mark_raw(value):
    pass


def effect_scope(detached: bool) -> "EffectScope":
    pass


def get_current_scope() -> "EffectScope":
    pass


def on_scope_dispose():
    pass


def computed(getter, debugger_options) -> Ref:
    pass


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


