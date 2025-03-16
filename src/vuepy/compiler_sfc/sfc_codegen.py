# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

import dataclasses
import pathlib
from typing import Any
from typing import Callable
from typing import List
from typing import Tuple

from ipywidgets import CallbackDispatcher

from vuepy.compiler_sfc.codegen import Dom
from vuepy.compiler_sfc.codegen import SetupContext
from vuepy.compiler_sfc.codegen import VNode
from vuepy.compiler_sfc.codegen import VueComponent
from vuepy.compiler_sfc.codegen import logger
from vuepy.reactivity.effect_scope import EffectScope
from vuepy.runtime.core.api_lifecycle import OnBeforeMount
from vuepy.runtime.core.api_lifecycle import OnMounted
from vuepy.runtime.core.api_setup_helpers import DefineProp
from vuepy.runtime.core.api_setup_helpers import DefineProps
from vuepy.runtime.core.api_setup_helpers import defineEmits
from vuepy.runtime.core.api_setup_helpers import defineModel
from vuepy.utils.common import Nil


class SFCWidgetContainer(Dom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_mounted_dispatcher = CallbackDispatcher()
        self.on_before_mount_dispatcher = CallbackDispatcher()
        self.on_unmounted_dispatcher = CallbackDispatcher()
        self.on_before_unmount_dispatcher = CallbackDispatcher()


class SFC(VueComponent):
    ADD_EVENT_LISTENER_FN = '_s1_on'  # $on
    EMIT_FN = '_s1_emit'  # $emit

    def __init__(
            self,
            context: SetupContext | dict,
            props: dict,
            setup_ret: dict,
            template: str,
            app: "App",
            render: Callable[[SetupContext | dict, dict, dict], VNode] = None,
            file: str = None,
    ):
        super().__init__()
        self.app = app
        self.template = template
        self.setup_returned = setup_ret
        self._context = context
        self._props = props
        self._data: dict = setup_ret
        self._define_props = {}
        self._define_emits = {}
        self._render = render
        self.file = file
        self.scope: EffectScope = EffectScope(True)

        # setup define_x
        _emits, _on_fn = self._gen_widget_on_fn()
        _props_property = self._gen_widget_props_property()
        _model_update_events = self._gen_model_update_events()
        for _event in _model_update_events:
            _emits.add_event(_event)

        _sfc_container_cls = type('SfcContainer', (SFCWidgetContainer,), {
            **_props_property,
            self.ADD_EVENT_LISTENER_FN: _on_fn,
            self.EMIT_FN: _emits,
        })
        self.root: SFCWidgetContainer = _sfc_container_cls()
        self._init_static_props(context.get('attrs', {}))
        self._register_lifecycle_cb(self.root)

    def _init_static_props(self, attrs):
        if not self.define_props:
            return

        _, _props = self.define_props
        for prop_name in _props.prop_names:
            val = attrs.get(prop_name, Nil)
            if val is Nil:
                continue
            setattr(self.root, prop_name, val)

    def _register_lifecycle_cb(self, container: SFCWidgetContainer):
        for _, cb in self._get_var_by_type(OnBeforeMount):
            container.on_before_mount_dispatcher.register_callback(cb.callback)

        for _, cb in self._get_var_by_type(OnMounted):
            container.on_mounted_dispatcher.register_callback(cb.callback)

    def setup(self, props: dict = None, ctx=None, vm: 'App' = None):
        return self._data

    def _gen_model_update_events(self):
        return [_model.update_event for (_, _model) in self.define_models]

    def _gen_widget_props_property(self):
        def _get(prop: DefineProp):
            def _(this):
                return prop.value

            return _

        def _set(prop: DefineProp):
            def _(this, val):
                prop.value = val

            return _

        props = [model.prop for _, model in self.define_models]
        if self.define_props:
            props.extend(self.define_props[1].props)

        return {
            prop.name: property(_get(prop), _set(prop))
            for prop in props
        }

    def _gen_widget_on_fn(self):
        emits = self.define_emits[1] if self.define_emits else defineEmits([])

        def _on_fn(this, event, callback, remove=False):
            emits.add_event_listener(event, callback, remove)

        return emits, _on_fn

    @property
    def define_props(self) -> (str, DefineProps):
        ret = self._get_var_by_type(DefineProps, limit=1)
        return ret[0] if ret else []

    @property
    def define_emits(self) -> (str, defineEmits):
        ret = self._get_var_by_type(defineEmits, limit=1)
        return ret[0] if ret else []

    @property
    def define_models(self) -> List[(str, defineModel)]:
        return self._get_var_by_type(defineModel)

    def _get_var_by_type(self, define_type, limit: int = float('inf')) -> List[Tuple[str, Any]]:
        ret = []
        count = 0
        for var_name, var in self.setup_returned.items():
            if count >= limit:
                break
            if isinstance(var, define_type):
                ret.append((var_name, var))
                count += 1
        return ret

    def __repr__(self):
        return f"{self.__class__.__name__}<{pathlib.Path(self.file).name}> at {id(self)}"

    def render(self, ctx: SetupContext = None, props: dict = None, setup_returned: dict = None) -> VNode:
        logger.info(f"🔥 Rerender {self}")
        self.scope.clear()

        # beforeMount
        self.root.on_before_mount_dispatcher()

        # compile and render
        with self.scope:
            if self._render:
                dom = self._render(self._context, self._props, self.setup_returned)
            else:
                from vuepy.compiler_sfc.template_compiler import DomCompiler
                dom = DomCompiler(self, self.app).compile(self.template)

        self.root.children = [dom]

        # mounted
        self.root.on_mounted_dispatcher()

        return self.root


@dataclasses.dataclass
class SFCType:
    # (props: dict, context: SetupContext, app: App) -> dict | Callable[[], h]:
    setup: Callable[[dict, SetupContext | dict, 'App'], dict | Callable] = None
    template: str = ''
    # (self, ctx, props, setup_returned) -> VNode:
    render: Callable[[SetupContext | dict, dict, dict], VNode] = None
    _file: str = ''

    def gen(self, props: dict, context: SetupContext | dict, app: "App") -> "SFC":
        setup_ret = self.setup(props, context, app) if self.setup else {}
        return SFC(context, props, setup_ret, self.template, app, self.render, self._file)
