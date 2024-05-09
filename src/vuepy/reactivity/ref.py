from vuepy.reactivity import Ref
from vuepy.reactivity import createDep
from vuepy.reactivity import effect
from vuepy.reactivity import effect
from vuepy.reactivity import is_readonly
from vuepy.reactivity.effect import DEP_STORE
from vuepy.reactivity.reactive import toReactive
from vuepy.reactivity import to_raw
from vuepy.reactivity import to_raw
from vuepy.reactivity.effect import trackEffects
from vuepy.reactivity.effect import triggerEffects
from vuepy.utils.general import has_changed


def ref(value) -> Ref:
    return createRef(value, False)


def shallow_ref(value) -> "ShallowRef":
    return createRef(value, True)


def createRef(raw_value, shallow: bool):
    if is_ref(raw_value):
        return raw_value

    return RefImpl(raw_value, shallow)


class RefImpl:
    def __init__(self, value, is_shallow):
        self._is_shallow = is_shallow
        self._raw_value = value if is_shallow else to_raw(value)
        self._value = value if is_shallow else _to_reactive(value)

    @property
    def value(self):
        trackRefValue(self)
        return self._value

    @value.setter
    def value(self, new_val):
        use_direct_value = self._is_shallow or isShallow(new_val) or is_readonly(new_val)
        new_val = new_val if use_direct_value else to_raw(new_val)
        if has_changed(new_val, self._raw_value):
            self._raw_value = new_val
            self._value = new_val if use_direct_value else toReactive(new_val)
            triggerRefValue(self, new_val)


def trackRefValue(ref):
    if effect.shouldTrack and effect.activeEffect:
        # ??
        ref = to_raw(ref)
        # __DEV__
        # dep = getattr(ref, 'dep', None)
        # if dep is None:
        #     dep = createDep()
        #     # todo dep不能挂在原始对象上
        #     ref.dep = dep
        dep = DEP_STORE.get(ref)
        trackEffects(dep)


def triggerRefValue(ref, new_val=None):
    ref = to_raw(ref)
    # todo dep不能挂在原始对象上
    # dep = getattr(ref, 'dep', None)
    # if dep is None:
    #     return
    if ref not in DEP_STORE:
        return
    # __DEV__
    dep = DEP_STORE.get(ref)
    triggerEffects(dep)


def is_ref(r) -> bool:
    pass


def unref(ref):
    return ref.value if is_ref(ref) else ref


def to_ref(value):
    pass


def to_value(source):
    pass


def to_refs(obj):
    pass