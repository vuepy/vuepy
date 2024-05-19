from __future__ import annotations

from vuepy import log
from vuepy.reactivity import config
from vuepy.reactivity import effect
from vuepy.reactivity.effect import DepStore
from vuepy.reactivity.effect import TrackOpTypes
from vuepy.reactivity.effect import TriggerOpTypes
from vuepy.reactivity.effect import trackEffects
from vuepy.reactivity.effect import triggerEffects
from vuepy.reactivity.reactive import isReadonly
from vuepy.reactivity.reactive import isShallow
from vuepy.reactivity.reactive import toReactive
from vuepy.reactivity.reactive import to_raw
from vuepy.utils.common import has_changed

logger = log.getLogger()

g_DEP_STORE = DepStore()


def ref(value, debug_msg='') -> "RefImpl":
    return createRef(value, False, debug_msg=debug_msg)


def shallow_ref(value) -> "ShallowRef":
    return createRef(value, True)


def createRef(raw_value, shallow: bool, debug_msg=''):
    if is_ref(raw_value):
        return raw_value

    return RefImpl(raw_value, shallow, debug_msg=debug_msg)


class RefImpl:
    def __init__(self, value, is_shallow, debug_msg=''):
        self._is_shallow = is_shallow
        self._raw_value = value if is_shallow else to_raw(value)
        self._value = value if is_shallow else toReactive(value)
        self.debug_msg = debug_msg

    @property
    def value(self):
        trackRefValue(self)
        return self._value

    @value.setter
    def value(self, new_val):
        use_direct_value = self._is_shallow or isShallow(new_val) or isReadonly(new_val)
        new_val = new_val if use_direct_value else to_raw(new_val)
        logger.debug('%s set value %s to %s', self, self._raw_value, new_val)
        if has_changed(new_val, self._raw_value):
            self._raw_value = new_val
            self._value = new_val if use_direct_value else toReactive(new_val)
            triggerRefValue(self, new_val)

    def __repr__(self):
        return f"RefImpl:{self.debug_msg} at {id(self)}"


def trackRefValue(ref):
    if effect.shouldTrack and effect.activeEffect:
        dep = g_DEP_STORE.get_or_create(ref)
        debugger_event = config.__DEV__ and {
            'target': ref,
            'type': TrackOpTypes.GET,
            'key': 'value',
        }
        trackEffects(dep, debugger_event)


def triggerRefValue(ref, new_val=None):
    dep = g_DEP_STORE.get(ref)
    if not dep:
        return

    debugger_event = config.__DEV__ and {
        'target': ref,
        'type': TriggerOpTypes.SET,
        'key': 'value',
        'newValue': new_val,
    }
    triggerEffects(dep, debugger_event)


def is_ref(r) -> bool:
    return isinstance(r, RefImpl)


def unref(ref):
    return ref.value if is_ref(ref) else ref


def to_ref(value):
    pass


def to_value(source):
    pass


def to_refs(obj):
    pass
