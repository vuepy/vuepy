from __future__ import annotations

import abc
import dataclasses
import pathlib
from typing import Any
from typing import Callable
from typing import List
from typing import Tuple
from typing import Type

import ipywidgets as widgets
from ipywidgets import CallbackDispatcher

from vuepy import log
from vuepy.compiler_core.ast import NodeAst
from vuepy.compiler_core.ast import VueCompAst
from vuepy.compiler_core.utils import VueCompNamespace
from vuepy.reactivity.effect_scope import EffectScope
from vuepy.reactivity.reactive import to_raw
from vuepy.reactivity.ref import RefImpl
from vuepy.reactivity.watch import WatchOptions
from vuepy.reactivity.watch import watch
from vuepy.runtime.core.api_lifecycle import OnBeforeMount
from vuepy.runtime.core.api_lifecycle import OnMounted
from vuepy.runtime.core.api_setup_helpers import DefineProp
from vuepy.runtime.core.api_setup_helpers import DefineProps
from vuepy.runtime.core.api_setup_helpers import defineEmits
from vuepy.runtime.core.api_setup_helpers import defineModel
from vuepy.utils.common import Nil
from vuepy.utils.common import has_changed

logger = log.getLogger()


class Dom(widgets.VBox):
    """
    https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def appendChild(self, el):
        self.children = self.children + (el,)
        return el

    def appendLeftChild(self, el):
        self.children = (el,) + self.children
        return el


class SetupContext:
    def __init__(self):
        self.attrs = {}
        self.slots = {}
        # 触发事件
        self.emit = {}
        # 暴露公共属性
        self.expose = {}


class VNode:
    def __init__(self, type_, props, children=None, key=''):
        self.type = type_
        self.props = props
        self.children = children
        self.key = key


class VueComponent(metaclass=abc.ABCMeta):
    _name = ''
    props = {}
    template = ''

    v_model_default = 'value'

    def __init__(self, setup_ret: dict = None, template: str = '', app: "App" = None):
        self.template = template
        self._data: dict = setup_ret
        self.app = app

    @classmethod
    def name(cls):
        # return (cls._name or cls.__name__).lower()
        return cls._name or cls.__name__

    def setup(self, props: dict = None, ctx=None, vm: 'App' = None):
        """

        :param props:
        :param ctx: attrs, slots, emit
        :param vm:
        :return:
        """
        pass

    def component(self, name: str):
        comp = self.to_ns().get(name)
        try:
            if comp and (isinstance(comp, SFCFactory) or issubclass(comp, VueComponent)):
                return comp
        except Exception as e:
            logger.debug(f"find component({name}) in Component `{self.name()}` failed, {e}.")
            pass

        comp = self.app.component(name)
        return comp

    def to_ns(self):
        return {
            **self.app.config.globalProperties.to_ns(),
            **self._data,
        }

    def render(self, ctx, props, setup_returned) -> VNode:
        """
        h(tag, props|attrs, children)

        :param ctx: attrs, slots, emit
        :param setup_returned:
        :param props:
        :return:
        """
        # if not self.template:
        #     return None
        # return vue_compiler_dom(self.template)
        pass


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

        _sfc_container = type('sfc_container', (SFCWidgetContainer,), {
            **_props_property,
            self.ADD_EVENT_LISTENER_FN: _on_fn,
            self.EMIT_FN: _emits,
        })
        self.root: SFCWidgetContainer = _sfc_container()
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
                from vuepy.compiler_sfc.compile_template import DomCompiler
                dom = DomCompiler(self, self.app).compile(self.template)

        self.root.children = [dom]

        # mounted
        self.root.on_mounted_dispatcher()

        return self.root


@dataclasses.dataclass
class SFCFactory:
    # (props: dict, context: SetupContext, app: App) -> dict | Callable[[], h]:
    setup: Callable[[dict, SetupContext | dict, 'App'], dict | Callable] = None
    template: str = ''
    # (self, ctx, props, setup_returned) -> VNode:
    render: Callable[[SetupContext | dict, dict, dict], VNode] = None
    _file: str = ''

    def gen(self, props: dict, context: SetupContext | dict, app: "App") -> "SFC":
        setup_ret = self.setup(props, context, app) if self.setup else {}
        return SFC(context, props, setup_ret, self.template, app, self.render, self._file)


class VueCompCodeGen:
    """
    h()
    """

    @classmethod
    def gen(
            cls,
            node: NodeAst,
            vm: 'VueComponent',
            ns: VueCompNamespace,
            app: "App"
    ):
        comp_ast = VueCompAst.transform(node.tag, node.attrs)
        # v-if
        if comp_ast.v_if:
            dummy = widgets.VBox()

            def _if_cond():
                return comp_ast.v_if.eval(ns)

            @watch(_if_cond, WatchOptions(immediate=True))
            def _change_v_if_widget(cond, old, on_cleanup):
                dummy.children = (cls._gen(comp_ast, node.children, vm, ns, app),) if cond else ()

            return dummy
        # v-show
        elif comp_ast.v_show:
            dummy = widgets.VBox()
            w = cls._gen(comp_ast, node.children, vm, ns, app)

            def _if_show():
                return comp_ast.v_show.eval(ns)

            @watch(_if_show, WatchOptions(immediate=True))
            def _show_widget(curr_show, old, on_cleanup):
                dummy.children = (w,) if curr_show else ()

            return dummy
        else:
            return cls._gen(comp_ast, node.children, vm, ns, app)

    @classmethod
    def _gen(
            cls,
            comp_ast: VueCompAst,
            children,
            vm: 'VueComponent',
            ns: VueCompNamespace,
            app: "App"
    ):
        component_cls: Type[VueComponent] = vm.component(comp_ast.tag)
        slots = {'default': []}
        for child in children or []:
            slot_name = getattr(child, 'v_slot', 'default')
            if slot_name == 'default':
                slots[slot_name].append(child)
            else:
                slots[slot_name] = child

        ctx = {
            'attrs': comp_ast.kwargs,
            'slots': slots,
            'emit': '',
        }
        props = {
            widget_attr: exp_ast.eval(ns)
            for widget_attr, exp_ast in comp_ast.v_binds.items()
        }

        if isinstance(component_cls, SFCFactory):
            component = component_cls.gen(props, ctx, app)
        else:
            component = component_cls()
        widget = component.render(ctx, props, {})

        if comp_ast.tag == 'slot' and isinstance(vm, SFC):
            _slot_name = comp_ast.kwargs.get('name', 'default')
            _slot = vm._context.get('slots', {}).get(_slot_name)
            if _slot:
                widget.children = _slot

        # v-slot
        if comp_ast.v_slot:
            widget.v_slot = comp_ast.v_slot

        # v-bind:
        for widget_attr, exp_ast in comp_ast.v_binds.items():
            if widget_attr == 'style' and hasattr(widget, 'css_style'):
                widget_attr = 'css_style'

            def _get_v_bind_value(_exp_ast=exp_ast):
                return _exp_ast.eval(ns)

            @watch(_get_v_bind_value, WatchOptions(immediate=True))
            def _v_bind_update_vm_to_view(curr, old, on_cleanup, _widget_attr=widget_attr):
                _old_val = to_raw(getattr(widget, _widget_attr, Nil))
                curr = to_raw(curr)
                if has_changed(curr, _old_val):
                    setattr(widget, _widget_attr, curr)

        # v-model:define-model=bind
        for _model_key, attr_chain in comp_ast.v_model:
            # :bind, parent to child
            # widget_attr = component_cls.v_model_default  # VueCompTag.v_model(comp_ast.tag)
            widget_attr = _model_key
            if _model_key == defineModel.DEFAULT_KEY and hasattr(component_cls, 'v_model_default'):
                widget_attr = getattr(component_cls, 'v_model_default')

            def _get_v_model_value(_attr_chain=attr_chain):
                return to_raw(ns.getattr(_attr_chain))

            @watch(_get_v_model_value, WatchOptions(immediate=True))
            def _v_model_update_vm_to_view(curr, old, on_cleanup, _widget_attr=widget_attr):
                _old_val = to_raw(getattr(widget, _widget_attr, Nil))
                curr = to_raw(curr)
                if has_changed(curr, _old_val):
                    setattr(widget, _widget_attr, curr)

            # v-on, child to parent
            def listener(_vm, _obj, _attr):
                def _(change):
                    val = change['new'] if isinstance(change, dict) else change
                    setattr(_obj, _attr, val)
                    if isinstance(_obj, defineModel) and isinstance(_vm, SFC):
                        logger.debug("%s emit(%s, %s)", _vm, _obj.update_event, val)
                        getattr(_vm.root, SFC.EMIT_FN)(_obj.update_event, val)

                return _

            obj, attr = ns.get_obj_and_attr(attr_chain)
            cls.add_event_listener(
                widget,
                f'update:{widget_attr}',
                listener(vm, obj, attr),
            )

        # v-on
        for ev, func_ast in comp_ast.v_on.items():
            def _event_handle(*args, _func_ast=func_ast, **kwargs):
                return _func_ast.eval(ns, {'__vp_args': args, '__vp_kwargs': kwargs})

            cls.add_event_listener(widget, ev, _event_handle)

        if comp_ast.v_ref:
            _ref = ns.getattr(comp_ast.v_ref)
            # if not isinstance(_ref, VueRef):
            if not isinstance(_ref, RefImpl):
                logger.error(f'v-ref={comp_ast.v_ref} needs to be of type Ref.')
            else:
                _ref.value = component if isinstance(component_cls, SFCFactory) else widget

        return widget

    @staticmethod
    def add_event_listener(widget, event, listener):
        if hasattr(widget, SFC.ADD_EVENT_LISTENER_FN):  # SFC
            getattr(widget, SFC.ADD_EVENT_LISTENER_FN)(event, listener)
        elif event.startswith('update:'):  # anywidget, ipyw
            attr = event.split(':', 1)[1]
            widget.observe(listener, names=attr)
        else:  # ipyw click
            getattr(widget, f"on_{event}")(listener)
