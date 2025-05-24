# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

import dataclasses
import pathlib
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple

from vuepy.compiler_sfc.codegen_backends.backend import INode
from vuepy.compiler_sfc.codegen_backends.backend import SFCLifeCycle, ISFCNode
from vuepy.compiler_sfc.codegen import SetupContext
from vuepy.compiler_sfc.codegen import VNode
from vuepy.compiler_sfc.codegen import VueComponent
from vuepy.compiler_sfc.codegen import logger
from vuepy.reactivity.effect_scope import EffectScope
from vuepy.runtime.core.api_lifecycle import OnBeforeMount
from vuepy.runtime.core.api_lifecycle import OnMounted
from vuepy.runtime.core.api_setup_helpers import DefineProps
from vuepy.runtime.core.api_setup_helpers import defineEmits
from vuepy.runtime.core.api_setup_helpers import defineModel
from vuepy.utils.common import Nil


class SFC(VueComponent):
    # ADD_EVENT_LISTENER_FN = '_s1_on'  # $on
    # EMIT_FN = '_s1_emit'  # $emit

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

        props = self._get_props()
        emitter = self.define_emits[1] if self.define_emits else defineEmits([])
        for event in self._get_events():
            emitter.add_event(event)

        self.sfc_widget_node: ISFCNode = self.app.codegen_backend.gen_sfc_widget_node(props, emitter)
        self._init_static_props(context.get('attrs', {}))

        for _, cb in self._get_var_by_type(OnBeforeMount):
            self.sfc_widget_node.on(SFCLifeCycle.ON_BEFORE_MOUNT, cb.callback)
        for _, cb in self._get_var_by_type(OnMounted):
            self.sfc_widget_node.on(SFCLifeCycle.ON_MOUNTED, cb.callback)

    def _init_static_props(self, attrs):
        if not self.define_props:
            return

        _, _props = self.define_props
        for prop_name in _props.prop_names:
            val = attrs.get(prop_name, Nil)
            if val is Nil:
                continue
            self.sfc_widget_node.setattr(prop_name, val)

    def setup(self, props: dict = None, ctx=None, vm: 'App' = None):
        return self._data
    
    def _get_events(self):
        events = list(SFCLifeCycle)
        events.extend([_model.update_event for (_, _model) in self.define_models])
        return events
    
    def _get_props(self):
        props = [model.prop for _, model in self.define_models]
        if self.define_props:
            props.extend(self.define_props[1].props)
        return {
            prop.name: prop for prop in props
        }

    # def _gen_model_update_events(self):
    #     return [_model.update_event for (_, _model) in self.define_models]
    #
    # def _gen_widget_props_property(self):
    #     def _get(prop: DefineProp):
    #         def _(this):
    #             return prop.value
    #
    #         return _
    #
    #     def _set(prop: DefineProp):
    #         def _(this, val):
    #             prop.value = val
    #
    #         return _
    #
    #     props = [model.prop for _, model in self.define_models]
    #     if self.define_props:
    #         props.extend(self.define_props[1].props)
    #
    #     return {
    #         prop.name: property(_get(prop), _set(prop))
    #         for prop in props
    #     }

    @property
    def define_props(self) -> Tuple[str, DefineProps]:
        ret = self._get_var_by_type(DefineProps, limit=1)
        return ret[0] if ret else []

    @property
    def define_emits(self) -> Tuple[str, defineEmits]:
        # todo raise error if define_emits get more than 1
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
        return f"{self.__class__.__name__}<{pathlib.Path(self.file).name}> "\
               f"at {hex(id(self))}"

    def _convert_slot_nodes_to_widgets(self, slots: Dict):
        pass

    def render(
        self,
        ctx: SetupContext = None,
        props: dict = None,
        setup_returned: dict = None
    ) -> INode:
        logger.info(f"🔥 Rerender {self}")
        self.scope.clear()

        # beforeMount
        self.sfc_widget_node.emit(SFCLifeCycle.ON_BEFORE_MOUNT)

        # compile and render
        with self.scope:
            if self._render:
                dom = self._render(self._context, self._props, self.setup_returned)
            else:
                from vuepy.compiler_sfc.template_compiler import DomCompiler
                dom = DomCompiler(self, self.app).compile(self.template)

        self.sfc_widget_node.replace_children([dom])

        # mounted
        self.sfc_widget_node.emit(SFCLifeCycle.ON_MOUNTED)

        return self.sfc_widget_node


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
