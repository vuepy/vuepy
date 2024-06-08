from __future__ import annotations

from typing import Any
from typing import Callable

from vuepy.reactivity import config
from vuepy.reactivity.dep import Dep
from vuepy.reactivity.effect import DebuggerOptions
from vuepy.reactivity.effect import ReactiveEffect
from vuepy.reactivity.ref import RefImpl
from vuepy.reactivity.ref import trackRefValue
from vuepy.reactivity.ref import triggerRefValue


ComputedGetter = Callable[[], Any]


class ComputedRefImpl(RefImpl):
    def __init__(self, getter: ComputedGetter, setter=None):
        self._dirty = True
        self.dep: Dep = None

        self.effect = ReactiveEffect(getter, scheduler=self.scheduler)
        self.effect.computed = self
        self._setter = setter
        self.is_readonly = setter is None
        self._value = None
        self.debug_msg = 'computed'

    def scheduler(self):
        if not self._dirty:
            self._dirty = True
            triggerRefValue(self)

    @property
    def value(self):
        trackRefValue(self)
        if self._dirty:
            self._dirty = False
            self._value = self.effect.run()

        return self._value

    @value.setter
    def value(self, new_val):
        if self.is_readonly:
            # todo
            print("warning")
        else:
            self._setter(new_val)


class WritableComputedOptions:
    def get(self) -> Any:
        pass

    def set(self, val: Any) -> None:
        pass


def computed(getter_or_options_or_debugger_options=None, debugger_options=None):
    is_decorator_no_arg = (getter_or_options_or_debugger_options, debugger_options) == (None, None)
    is_decorator_with_arg = isinstance(getter_or_options_or_debugger_options, DebuggerOptions)
    # @computed() or @computed(debuggerOptions)
    if is_decorator_with_arg or is_decorator_no_arg:
        def wrap(fn):
            return computed_impl(fn, getter_or_options_or_debugger_options)

        return wrap
    # @computed or computed()
    else:
        return computed_impl(getter_or_options_or_debugger_options, debugger_options)


def computed_impl(getter_or_options, debugger_options: DebuggerOptions = None) -> ComputedRefImpl:
    if isinstance(getter_or_options, WritableComputedOptions):
        getter = getter_or_options.get
        setter = getter_or_options.set
    else:
        getter = getter_or_options
        setter = None

    c_ref = ComputedRefImpl(getter, setter)
    if config.__DEV__ and debugger_options:
        c_ref.effect.onTrack = debugger_options.onTrack
        c_ref.effect.onTrigger = debugger_options.onTrigger

    return c_ref
