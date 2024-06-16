from __future__ import annotations

import dataclasses
import enum
from typing import Any
from typing import Callable
from typing import List
from typing import Union

from vuepy.reactivity import config
from vuepy.reactivity.computed import ComputedRefImpl
from vuepy.reactivity.constant import ErrorCodes
from vuepy.reactivity.effect import DebuggerOptions
from vuepy.reactivity.effect import ReactiveEffect
from vuepy.reactivity.reactive import ReactiveProxy
from vuepy.reactivity.reactive import ReactiveFlags
from vuepy.reactivity.reactive import isShallow
from vuepy.reactivity.reactive import is_reactive
from vuepy.reactivity.ref import RefImpl
from vuepy.reactivity.ref import isRef
from vuepy.utils.common import Nil
from vuepy.utils.common import gen_hash_key
from vuepy.utils.common import has_changed

OnCleanUp = Callable[[Callable[[], None]], None]  # (cleanupFn: () => void) => void
WatchEffect = Callable[[OnCleanUp], None]  # (onCleanup: OnCleanup) => void
WatchSource = Union[RefImpl, ComputedRefImpl, Callable[[], Any], ReactiveProxy]
# (val: Any, oldVal: Any, onCleanup: OnCleanup) => any
WatchCallback = Callable[[Any, Any, OnCleanUp], Any]
MultiWatchSources = List[WatchSource]
WatchStopHandle = Callable[[], None]  # () => void


class FlushEnum(enum.Enum):
    PRE = 'pre'
    POST = 'post'
    SYNC = 'sync'


@dataclasses.dataclass
class WatchOptionsBase(DebuggerOptions):
    flush: FlushEnum = FlushEnum.PRE


@dataclasses.dataclass
class WatchOptions(WatchOptionsBase):
    immediate: bool = False
    deep: bool = False


def watchEffect(
        effect_or_options: WatchEffect | WatchOptions = None,
        debuggerOptions: DebuggerOptions = None
) -> WatchStopHandle:
    is_decorator_no_arg = (effect_or_options, debuggerOptions) == (None, None)
    is_decorator_with_arg = isinstance(effect_or_options, DebuggerOptions)
    # @watchEffect() or @watchEffect(debuggerOptions)
    if is_decorator_no_arg or is_decorator_with_arg:
        def wrap(fn):
            return watchEffect_impl(fn, effect_or_options)

        return wrap
    # @watchEffect or watchEffect()
    else:
        return watchEffect_impl(effect_or_options, debuggerOptions)


def watchEffect_impl(watch_effect: WatchEffect, options: WatchOptionsBase = None) -> WatchStopHandle:
    options = options or WatchOptionsBase()
    flush = options.flush
    onTrack = options.onTrack
    onTrigger = options.onTrigger

    instance = None

    cleanup = None

    def onCleanup(fn):
        nonlocal cleanup

        def _cleanup():
            nonlocal cleanup
            callWithErrorHandling(fn, instance, ErrorCodes.WATCH_CLEANUP)
            cleanup = None
            effect.onStop = None

        cleanup = _cleanup
        effect.onStop = _cleanup

    def getter():
        if instance and instance.isUnmounted:
            return
        cleanup and cleanup()
        return callWithErrorHandling(watch_effect, instance, ErrorCodes.WATCH_CALLBACK, [onCleanup])

    def job():
        if not effect.active:
            return
        effect.run()

    job.allowRecurse = False
    if flush == FlushEnum.SYNC:
        scheduler = job
    elif flush == FlushEnum.POST:
        scheduler = job
    else:
        scheduler = job

    effect = ReactiveEffect(getter, scheduler)
    if config.__DEV__:
        effect.onTrack = onTrack
        effect.onTrigger = onTrigger

    # initial run
    if flush == FlushEnum.POST:
        # queuePostRenderEffect()
        pass
    else:
        effect.run()

    def unwatch():
        effect.stop()
        if instance and instance.scope:
            instance.scope.effects.pop(effect)

    return unwatch


def watch(
        source: WatchSource | MultiWatchSources,
        cb_or_options: WatchCallback | WatchOptions = None,
        options: WatchOptions = None
) -> WatchStopHandle:
    is_decorator_src = (cb_or_options, options) == (None, None)
    is_decorator_src_options = isinstance(cb_or_options, WatchOptions)
    # @watch(src) or @watch(src, options)
    if is_decorator_src or is_decorator_src_options:
        def wrap(fn):
            return doWatch(source, fn, cb_or_options)

        return wrap
    # watch(src, cb) or watch(src, cb, options)
    else:
        return doWatch(source, cb_or_options, options)


def doWatch(
        source: WatchSource | List[WatchSource] | WatchEffect,
        cb: WatchCallback,
        watch_options: WatchOptions = None,
) -> WatchStopHandle:
    watch_options = watch_options or WatchOptions()
    immediate = watch_options.immediate
    deep = watch_options.deep
    flush = watch_options.flush
    onTrack = watch_options.onTrack
    onTrigger = watch_options.onTrigger

    # todo
    instance = None
    getter = None
    forceTrigger = False
    isMultiSource = False

    if isRef(source):
        getter = lambda: source.value
        forceTrigger = isShallow(source)
    elif is_reactive(source):
        getter = lambda: source
        deep = True
    elif isinstance(source, list):
        isMultiSource = True
        forceTrigger = any(is_reactive(s) or isShallow(s) for s in source)

        def getter():
            _ret = []
            for s in source:
                if isRef(s):
                    _ret.append(s.value)
                elif is_reactive(s):
                    _ret.append(traverse(s))
                elif callable(s):
                    _ret.append(callWithErrorHandling(s, instance, ErrorCodes.WATCH_GETTER))
                else:
                    config.__DEV__ and print(f"Invalid watch source: {source}.")
            return _ret

    elif callable(source):
        getter = lambda: callWithErrorHandling(source, instance, ErrorCodes.WATCH_GETTER)
    else:
        getter = lambda: None
        config.__DEV__ and print(f"Invalid watch source: {source}.")

    if cb and deep:
        baseGetter = getter
        getter = lambda: traverse(baseGetter())

    cleanup = None

    def onCleanup(fn):
        nonlocal cleanup

        def _cleanup():
            nonlocal cleanup
            callWithErrorHandling(fn, instance, ErrorCodes.WATCH_CLEANUP)
            cleanup = None
            effect.onStop = None

        cleanup = _cleanup
        effect.onStop = _cleanup

    oldValue = [Nil] * len(source) if isMultiSource else Nil

    def job():
        nonlocal oldValue
        if not effect.active:
            return

        newValue = effect.run()
        if isMultiSource:
            had_change = any(has_changed(n, o) for (n, o) in zip(newValue, oldValue))
        else:
            had_change = has_changed(newValue, oldValue)

        if deep or forceTrigger or had_change:
            cleanup and cleanup()

            if oldValue is Nil:
                _old_val = None
            else:
                _old_val = [] if isMultiSource and (oldValue[0] is Nil) else oldValue
            _args = [newValue, _old_val, onCleanup]
            callWithErrorHandling(cb, instance, ErrorCodes.WATCH_CALLBACK, _args)
            oldValue = newValue

    job.allowRecurse = True
    if flush == FlushEnum.SYNC:
        scheduler = job
    elif flush == FlushEnum.POST:
        scheduler = job
    else:
        scheduler = job

    effect = ReactiveEffect(getter, scheduler)
    if config.__DEV__:
        effect.onTrack = onTrack
        effect.onTrigger = onTrigger

    # initial run
    if immediate:
        job()
    else:
        oldValue = effect.run()

    def unwatch():
        effect.stop()
        if instance and instance.scope:
            instance.scope.effects.pop(effect)

    return unwatch


@dataclasses.dataclass
class SchedulerJob:
    id: int = None
    pre: bool = False
    active: bool = False
    computed: bool = False
    allowRecurse: bool = False
    # ownerInstance: ComponentInternalInstance = None


def callWithErrorHandling(fn, instance, type, args: List = None):
    res = None
    try:
        res = fn(*args) if args else fn()
    except Exception as err:
        print(f"call {fn}({ args }) {type} failed, {err}")
        raise err
    return res


def traverse(value, seen: set = None):
    if not is_reactive(value) or getattr(value, ReactiveFlags.SKIP.value, False):
        return value

    seen = seen or set()
    value_hash = gen_hash_key(value)
    if value_hash in seen:
        return value

    seen.add(value_hash)
    if isRef(value):
        traverse(value.value, seen)
    elif isinstance(value, list):
        for val in value:
            traverse(val, seen)
    elif isinstance(value, dict):
        for val in value.values():
            traverse(val, seen)
    # todo
    # elif isPlaninObject(value):
    #     for key in value:
    #         traverse(getattr(value, key, None), seen)

    return value
