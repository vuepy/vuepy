from __future__ import annotations

import inspect
from typing import List

from ipywidgets import CallbackDispatcher

from vuepy import log
from vuepy.reactivity.ref import ref

logger = log.getLogger()


def defineProps(props: dict | list):
    """
    props = defineProps('p1')
    props.p1.value
    """
    frame = inspect.currentframe().f_back
    caller_args = get_caller_args(frame)
    init_props = caller_args[0] if caller_args else {}
    init_attrs = caller_args[1].get('attrs', {}) if len(caller_args) >= 2 else {}
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
        if cb_dispatcher:
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
        handlers = self.events_to_cb_dispatcher.get(event)
        if not handlers:
            raise Exception(f"Event {event} not supported.")
        handlers(*args, **kwargs)


class defineModel:
    """
    count = defineModel("count")
    count.value += 1
    """
    # DEFAULT_KEY = 'modelValue'
    DEFAULT_KEY = 'value'

    def __init__(self, model_key: str | dict = DEFAULT_KEY):
        self.model_key = model_key
        self.prop = DefineProp(model_key)
        self.update_event = f'update:{self.model_key}'

    @property
    def value(self):
        return self.prop.value

    @value.setter
    def value(self, val):
        logger.debug("defineModel:%s set value %s to %s", self.model_key, self.prop.value, val)
        self.prop.value = val


def get_caller_args(frame):
    if not frame:
        return []

    caller_name = frame.f_code.co_name
    caller_func = frame.f_globals.get(caller_name)
    if not caller_func:
        logger.warn(f"can't get caller_func<{caller_name}>")
        return []

    argspec = inspect.getfullargspec(caller_func)
    if not argspec.args:
        logger.warn(f"get caller_func<{caller_name}> args is None")
        return []

    return [frame.f_locals.get(arg_name) for arg_name in argspec.args]
