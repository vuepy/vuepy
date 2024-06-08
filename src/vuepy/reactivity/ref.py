from __future__ import annotations

from vuepy import log
from vuepy.reactivity import config
from vuepy.reactivity import effect
from vuepy.reactivity.effect import DepStore
from vuepy.reactivity.effect import TrackOpTypes
from vuepy.reactivity.effect import TriggerOpTypes
from vuepy.reactivity.effect import trackEffects
from vuepy.reactivity.effect import triggerEffects
from vuepy.reactivity.reactive import DictProxy
from vuepy.reactivity.reactive import ListProxy
from vuepy.reactivity.reactive import isReadonly
from vuepy.reactivity.reactive import isShallow
from vuepy.reactivity.reactive import toReactive
from vuepy.reactivity.reactive import to_raw
from vuepy.utils.common import has_changed

logger = log.getLogger()

g_DEP_STORE = DepStore()


def ref(value, debug_msg='') -> "RefImpl":
    return createRef(value, False, debug_msg=debug_msg)


def shallowRef(value) -> "ShallowRef":
    return createRef(value, True)


def createRef(raw_value, shallow: bool, debug_msg=''):
    if isRef(raw_value):
        return raw_value

    return ShallowRef(raw_value, debug_msg) if shallow else Ref(raw_value, debug_msg)


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


class Ref(RefImpl):
    def __init__(self, value, debug_msg=''):
        super().__init__(value, False, debug_msg)


class ShallowRef(RefImpl):
    def __init__(self, value, debug_msg=''):
        super().__init__(value, True, debug_msg)


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


def triggerRef(ref_obj: ShallowRef):
    triggerRefValue(ref_obj, ref_obj.value if config.__DEV__ else None)


# todo add Readonly
class GetterRefImpl(Ref):
    def __init__(self, _getter):
        self._getter = _getter
        self.debug_msg = 'GetterRefImpl'

    @property
    def value(self):
        return self._getter()


class ObjectRefImpl(Ref):
    def __init__(self, _object, _key, _default_val):
        self._object = _object
        self._key = _key
        self._default_val = _default_val

    @property
    def value(self):
        return self._object.get(self._key, self._default_val)

    @value.setter
    def value(self, new_val):
        self._object[self._key] = new_val


def isRef(val) -> bool:
    return isinstance(val, RefImpl)


def unref(ref_obj):
    return ref_obj.value if isRef(ref_obj) else ref_obj


def toRef(source, key: str = '', default_val=None) -> Ref:
    if isRef(source):
        return source
    elif callable(source):
        return GetterRefImpl(source)
    elif hasattr(source, key):
        return propertyToRef(source, key, default_val)
    else:
        return ref(source)


def propertyToRef(source, key, default_val=None):
    val = source[key]
    return val if isRef(val) else ObjectRefImpl(source, key, default_val)


def toValue(source):
    return source() if callable(source) else unref(source)


def toRefs(obj):
    if isinstance(obj, ListProxy):
        ret = []
        for i in range(len(obj)):
            ret.append(propertyToRef(obj, i))
        return ret
    elif isinstance(obj, DictProxy):
        ret = {}
        for key in obj:
            ret[key] = propertyToRef(obj, key)
        return ret
    else:
        logger.warn(f"toRefs() expects a reactive object but received a plain one.")
        return {}
