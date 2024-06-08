from __future__ import annotations

from typing import Any
from typing import Callable
from typing import List

from vuepy import log as logging
from vuepy.reactivity import config

logger = logging.getLogger()

activeEffectScope: "EffectScope" = None


class EffectScope:
    def __init__(self, detached=False):
        self.active = True
        # self.effects: List["ReactiveEffect"] = []
        self.effects = []
        self.detached = detached
        self.cleanups: List[Callable[[], None]] = []
        self.scopes: List[EffectScope] = []
        self.index: int = None

        self.parent = activeEffectScope
        if not self.detached and activeEffectScope:
            self.index = len(activeEffectScope.scopes)
            activeEffectScope.scopes.append(self)

    def run(self, fn: Callable[[], Any]) -> Any:  # (fn: () => T): T
        if self.active:
            with self:
                return fn()
        elif config.__DEV__:
            logger.warn('cannot run an inactive effect scope.')

    def on(self):
        """
        This should only be called on non-detached scopes
        :return:
        """
        global activeEffectScope
        activeEffectScope = self

    def off(self):
        """
        This should only be called on non-detached scopes
        :return:
        """
        global activeEffectScope
        activeEffectScope = self.parent

    def __enter__(self):
        global activeEffectScope

        self.parent = activeEffectScope
        activeEffectScope = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global activeEffectScope

        activeEffectScope = self.parent
        self.parent = None

    def clear(self):
        if not self.active:
            return

        for effect in self.effects:
            effect.stop()

        for cleanup in self.cleanups:
            cleanup()

        for scope in self.scopes:
            scope.stop(True)

    def stop(self, fromParent=False):
        if not self.active:
            return

        for effect in self.effects:
            effect.stop()

        for cleanup in self.cleanups:
            cleanup()

        for scope in self.scopes:
            scope.stop(True)

        if (not self.detached) and self.parent and (not fromParent):
            last = self.parent.scopes.pop() if self.parent.scopes else None
            if last and last is not self:
                if self.index < len(self.parent.scopes):
                    self.parent.scopes[self.index] = last
                last.index = self.index

        self.parent = None
        self.active = False


def effectScope(detached=False) -> EffectScope:
    return EffectScope(detached)


def recordEffectScope(effect, scope: "EffectScope" = None):
    if scope and scope.active:
        scope.effects.append(effect)


def getCurrentScope():
    return activeEffectScope


def onScopeDispose(fn: Callable[[], None]) -> None:
    if activeEffectScope:
        activeEffectScope.cleanups.append(fn)
    elif config.__DEV__:
        logger.warn("onScopeDispose() is called when there is no active effect scope to be associated with.")
