# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

import enum
import threading
from typing import Any


class LifecycleHooks(enum.Enum):
    BEFORE_CREATE = 'bc'
    CREATED = 'c'
    BEFORE_MOUNT = 'bm'
    MOUNTED = 'm'
    BEFORE_UPDATE = 'bu'
    UPDATED = 'u'
    BEFORE_UNMOUNT = 'bum'
    UNMOUNTED = 'um'
    DEACTIVATED = 'da'
    ACTIVATED = 'a'
    RENDER_TRIGGERED = 'rtg'
    RENDER_TRACKED = 'rtc'
    ERROR_CAPTURED = 'ec'
    SERVER_PREFETCH = 'sp'


class Hook:
    pass


# Thread-local storage for collecting lifecycle hooks during setup execution
_setup_context = threading.local()


def _get_active_setup_context():
    """Get the current active setup context."""
    if not hasattr(_setup_context, 'active'):
        return None
    return _setup_context.active


class SetupContext:
    """Context manager for collecting lifecycle hooks during setup execution.

    Supports nested usage similar to EffectScope. Each context maintains
    its own hooks dictionary and can store arbitrary data via get/set methods.
    """

    def __init__(self, app: "App"):
        self.app = app
        self.vars: dict[str, Any] = {}
        self.parent = None

    def get(self, key: str, default=None):
        return self.vars.get(key, default)

    def get_vars(self):
        return self.vars

    def set(self, key: str, value):
        self.vars[key] = value

    def __enter__(self):
        """Enter the context and set it as active."""
        # Save parent context
        self.parent = _get_active_setup_context()
        # Set this context as active
        _setup_context.active = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context and restore parent context."""
        # Restore parent context
        if self.parent is not None:
            _setup_context.active = self.parent
        elif hasattr(_setup_context, 'active'):
            delattr(_setup_context, 'active')
        self.parent = None
        # return False  # Don't suppress exceptions


class OnMounted:
    def __init__(self, callback):
        self.callback = callback
        # Automatically register to current setup context if available
        ctx = _get_active_setup_context()
        ctx.set(f"_{OnMounted.__name__}_{callback.__name__}_{id(self)}", self)

class OnBeforeMount:
    def __init__(self, callback):
        self.callback = callback
        # Automatically register to current setup context if available
        ctx = _get_active_setup_context()
        ctx.set(f"_{OnBeforeMount.__name__}_{callback.__name__}_{id(self)}", self)


class OnUnmounted:
    def __init__(self, callback):
        self.callback = callback
        # Automatically register to current setup context if available
        ctx = _get_active_setup_context()
        ctx.set(f"_{OnUnmounted.__name__}_{callback.__name__}_{id(self)}", self)


class OnBeforeUnmount:
    def __init__(self, callback):
        self.callback = callback
        # Automatically register to current setup context if available
        ctx = _get_active_setup_context()
        ctx.set(f"_{OnBeforeUnmount.__name__}_{callback.__name__}_{id(self)}", self)


def onMounted(callback):
    return OnMounted(callback)


def onBeforeMount(callback):
    return OnBeforeMount(callback)


def onUnmounted(callback):
    return OnUnmounted(callback)


def onBeforeUnmount(callback):
    return OnBeforeUnmount(callback)
