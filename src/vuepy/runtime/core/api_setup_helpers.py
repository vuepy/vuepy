# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

import inspect
from typing import Any, List

from vuepy import log
from vuepy.reactivity.ref import ref

logger = log.getLogger()


class CallbackDispatcher:
    """A structure for registering and running callbacks"""
    def __init__(self):
        self.callbacks: List[Any] = []

    def __call__(self, *args, **kwargs):
        """Call all of the registered callbacks."""
        value = None
        for callback in self.callbacks:
            try:
                local_value = callback(*args, **kwargs)
            except Exception as e:
                print(f"Exception in callback {callback}: {e}")
            else:
                value = local_value if local_value is not None else value
        return value

    def register_callback(self, callback, remove=False):
        """(Un)Register a callback

        Parameters
        ----------
        callback: method handle
            Method to be registered or unregistered.
        remove=False: bool
            Whether to unregister the callback."""

        # (Un)Register the callback.
        if remove and callback in self.callbacks:
            self.callbacks.remove(callback)
        elif not remove and callback not in self.callbacks:
            self.callbacks.append(callback)


def defineProps(props: dict | list):
    """
    def setup(props, ctx, app):
        props = defineProps('p1')
        props.p1.value
    ->
    def setup(props, ctx, app):
        init_props = props
        init_attrs = ctx.get('attrs', {})
        init_vals = {**init_props, **init_attrs}

        props = DefineProps(props, init_vals)
    """
    from vuepy.runtime.core.api_lifecycle import _get_active_setup_context
    active_ctx = _get_active_setup_context()

    # fix: in nuitka, get_caller_args returns [None, None, None], causing init_props and init_attrs to be empty
    if active_ctx and hasattr(active_ctx, '_vuepy_internal_props'):
        init_props = active_ctx._vuepy_internal_props
        ctx_obj = getattr(active_ctx, '_vuepy_internal_ctx', {})
        init_attrs = ctx_obj.get('attrs', {}) if isinstance(ctx_obj, dict) else {}
    else:
        frame = inspect.currentframe().f_back
        caller_args = get_caller_args(frame)
        init_props = caller_args[0] if caller_args and caller_args[0] is not None else {}
        init_attrs = caller_args[1].get('attrs', {}) if len(caller_args) >= 2 and caller_args[1] is not None else {}

    init_vals = {**init_props, **init_attrs}
    return DefineProps(props, init_vals)


class DefineProp:
    def __init__(self, prop_name: str, default=None):
        self.name = prop_name
        self._value = ref(default, debug_msg=f"prop:{prop_name}")

    @property
    def value(self):
        return self._value.value

    @value.setter
    def value(self, val):
        self._value.value = val


class DefineProps:
    def __init__(self, props: dict | list, init_vals: dict = None):
        self.prop_names = props
        self.props: List[DefineProp] = [
            DefineProp(name, init_vals.get(name)) for name in self.prop_names
        ]
        for prop in self.props:
            setattr(self, prop.name, prop)


class defineEmits:
    def __init__(self, events: List[str]):
        self.events = events
        self.events_to_cb_dispatcher: dict[str, CallbackDispatcher] = {}
        for event in self.events:
            self.add_event(event)

    def get_cb_dispatcher(self, event):
        return self.events_to_cb_dispatcher.get(event)

    def add_event(self, event):
        if event in self.events_to_cb_dispatcher:
            return
        self.events_to_cb_dispatcher[event] = CallbackDispatcher()

    def add_event_listener(self, event, callback, remove=False):
        cb_dispatcher = self.get_cb_dispatcher(event)
        # if cb_dispatcher:
        #     cb_dispatcher.register_callback(callback, remove)
        #     return
        if cb_dispatcher is None:
            self.add_event(event)
            cb_dispatcher = self.get_cb_dispatcher(event)

        cb_dispatcher.register_callback(callback, remove)

    def clear_events(self):
        self.events_to_cb_dispatcher = {}

    def __call__(self, event, *args, **kwargs):
        """$emit event.

        :param event:
        :param args: payload
        :param kwargs: payload
        :return:
        """
        cb_dispatcher = self.events_to_cb_dispatcher.get(event)
        logger.debug("defineEmits:%s emit(%s, %s)", self, event, args)
        if not cb_dispatcher:
            raise Exception(f"Event {event} not supported.")
        cb_dispatcher(*args, **kwargs)


class defineModel:
    """
    count = defineModel("count")
    count.value += 1
    """
    # DEFAULT_KEY = 'modelValue'
    DEFAULT_KEY = 'value'

    def __init__(self, model_key: str | dict = DEFAULT_KEY, value=None):
        self.model_key = model_key
        self.prop = DefineProp(model_key, value)
        self.update_event = f'update:{self.model_key}'
        self._emit: defineEmits = None

    @property
    def value(self):
        # TODO: hasOwn(props, name) ? props[name] : localRef.value
        return self.prop.value

    @value.setter
    def value(self, val):
        logger.debug("defineModel:%s set value %s to %s", self.model_key, self.prop.value, val)
        self.prop.value = val
        if self._emit:
            self._emit(self.update_event, val)
    
    def register_emit(self, emit):
        if self._emit:
            raise Exception(f"defineModel {self.model_key} already has emit {self.emit}")
        self._emit = emit
        self._emit.add_event(self.update_event)


def get_caller_args(frame):
    if not frame:
        return []

    caller_name = frame.f_code.co_name
    caller_func = frame.f_globals.get(caller_name)
    if not caller_func:
        logger.warning("can't get caller_func<%s>", caller_name)
        return []

    argspec = inspect.getfullargspec(caller_func)
    if not argspec.args:
        logger.warning("get caller_func<%s> args is None", caller_name)
        return []

    return [frame.f_locals.get(arg_name) for arg_name in argspec.args]
