# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

import asyncio
from collections.abc import Coroutine
from typing import Type

from vuepy import VueComponent
from vuepy import defineModel
from vuepy import watch
from vuepy.compiler_core.ast import NodeAst
from vuepy.compiler_core.ast import VueCompAst
from vuepy.compiler_core.utils import VueCompNamespace
from vuepy.compiler_dom.codegen import VueHtmlCompCodeGen
from vuepy.compiler_sfc.codegen_backends.backend import INode
from vuepy.compiler_sfc.sfc_codegen import SFC
from vuepy.compiler_sfc.sfc_codegen import SFCType
from vuepy.compiler_sfc.codegen import logger
from vuepy.reactivity.reactive import to_raw
from vuepy.reactivity.ref import RefImpl
from vuepy.reactivity.watch import WatchOptions
from vuepy.utils.common import Nil
from vuepy.utils.common import has_changed

# todo move compiler_dom/codegen.py over here


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
            # dummy = widgets.VBox()
            dummy: INode = app.codegen_backend.gen_widget_collection_node()

            def _if_cond():
                return comp_ast.v_if.eval(ns)

            @watch(_if_cond, WatchOptions(immediate=True))
            def _change_v_if_widget(cond, old, on_cleanup):
                # dummy.children = (cls._gen(comp_ast, node.children, vm, ns, app),) if cond else ()
                dummy.replace_children(
                    (cls._gen(comp_ast, node.children, vm, ns, app),) if cond else ())

            return dummy
        # v-show
        elif comp_ast.v_show:
            # dummy = widgets.VBox()
            dummy: INode = app.codegen_backend.gen_widget_collection_node()
            w = cls._gen(comp_ast, node.children, vm, ns, app)

            def _if_show():
                return comp_ast.v_show.eval(ns)

            @watch(_if_show, WatchOptions(immediate=True))
            def _show_widget(curr_show, old, on_cleanup):
                # dummy.children = (w,) if curr_show else ()
                dummy.replace_children((w,) if curr_show else ())

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
            child = VueHtmlCompCodeGen.gen_from_fn(child, app) if callable(child) else child
            if slot_name == 'default':
                slots[slot_name].append(child)
            else:
                slots[slot_name] = child

        ctx = {
            'attrs': {**comp_ast.kwargs},
            'slots': slots,
            'emit': '',
        }
        # get v-bind init value
        props = {
            widget_attr: exp_ast.eval(ns)
            for widget_attr, exp_ast in comp_ast.v_binds.items()
        }
        # get v-model init value
        for _model_key, _attr_chain in comp_ast.v_model:
            # :bind, parent to child
            # widget_attr = component_cls.v_model_default  # VueCompTag.v_model(comp_ast.tag)
            if _model_key == defineModel.DEFAULT_KEY and hasattr(component_cls, 'v_model_default'):
                _widget_attr = getattr(component_cls, 'v_model_default')
            else:
                _widget_attr = _model_key

            props[_widget_attr] = to_raw(ns.getattr(_attr_chain))

        if isinstance(component_cls, SFCType):
            component = component_cls.gen(props, ctx, app)
        else:
            component = component_cls()

        widget: INode = component.render(ctx, props, {})

        if comp_ast.tag == 'slot' and isinstance(vm, SFC):
            _slot_name = comp_ast.kwargs.get('name', 'default')
            _slot = vm._context.get('slots', {}).get(_slot_name)
            if _slot:
                # widget.children = _slot
                widget.replace_children(_slot)

        # v-slot
        if comp_ast.v_slot:
            widget.v_slot = comp_ast.v_slot

        # v-bind:
        for widget_attr, exp_ast in comp_ast.v_binds.items():
            # if widget_attr == 'style' and hasattr(widget, 'css_style'):
            if widget_attr == 'style' and widget.hasattr('css_style'):
                widget_attr = 'css_style'

            def _get_v_bind_value(_exp_ast=exp_ast):
                return _exp_ast.eval(ns)

            @watch(_get_v_bind_value, WatchOptions(immediate=True))
            def _v_bind_update_vm_to_view(curr, old, on_cleanup, _widget=widget, _widget_attr=widget_attr):
                # _old_val = to_raw(getattr(_widget, _widget_attr, Nil))
                _old_val = to_raw(_widget.getattr(_widget_attr, Nil))
                curr = to_raw(curr)
                if has_changed(curr, _old_val):
                    # setattr(_widget, _widget_attr, curr)
                    _widget.setattr(_widget_attr, curr)

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
            def _v_model_update_vm_to_view(curr, old, on_cleanup, _widget=widget, _widget_attr=widget_attr):
                # _old_val = to_raw(getattr(_widget, _widget_attr, Nil))
                _old_val = to_raw(_widget.getattr(_widget_attr, Nil))
                curr = to_raw(curr)
                logger.info(f'val changed curr: {curr}; old: {_old_val}')
                if has_changed(curr, _old_val):
                    # setattr(_widget, _widget_attr, curr)
                    _widget.setattr(_widget_attr, curr)

            # v-on, child to parent
            def listener(_vm, _obj, _attr):
                """
                <!-- Child.vue -->
                <script>
                model = defineModel('modelValue')
                compile to: #A
                    props = defineProps(['modelValue']) # 4
                    emit = defineEmits(['update:modelValue'])
                </script>

                <template>
                <input v-model="modelValue"/>
                compile to: #B
                    <input #0
                        :value="props.modelValue" 
                        @input="emit('update:modelValue', $event.target.value)" #1
                    />
                </template>

                <!-- Parent.vue -->
                <Child v-model="foo"/>
                compile to:
                    <Child
                    :modelValue="foo" #3
                    @update:modelValue="$event => (foo = $event)" #2
                    />

                child to parent steps:
                  #0 input change
                  #1 emit new value
                  #2 parent listen to child event and update foo
                  #3 parent pass foo to child
                  #4 child get foo from parent
                """
                def _(change):
                    if isinstance(change, dict):
                        val = change['new']
                    elif hasattr(change, 'new'):
                        val = change.new
                    else:
                        val = change

                    setattr(_obj, _attr, val)
                    # compile to: #B
                    if isinstance(_obj, defineModel) and isinstance(_vm, SFC):
                        logger.debug("%s emit(%s, %s)", _vm, _obj.update_event, val)
                        # step #1
                        # _vm.sfc_widget_node._s1_emit(_obj.update_event, val)
                        # getattr(_vm.sfc_widget_node, SFC.EMIT_FN)(_obj.update_event, val)
                        _vm.sfc_widget_node.emit(_obj.update_event, val)

                return _

            obj, attr = ns.get_obj_and_attr(attr_chain)
            if isinstance(obj, defineModel) and isinstance(vm, SFC):
                observe_name = obj.update_event
            else:
                observe_name = widget_attr
            widget.observe(wrap_callback(listener(vm, obj, attr)), observe_name)

            # cls.add_event_listener(
            #     widget,
            #     f'update:{widget_attr}',
            #     listener(vm, obj, attr),
            # )

        # v-on
        for ev, func_ast in comp_ast.v_on.items():
            def _event_handle(*args, _func_ast=func_ast, **kwargs):
                return _func_ast.eval(ns, {'__vp_args': args, '__vp_kwargs': kwargs})

            # cls.add_event_listener(widget, ev, _event_handle)
            widget.on(ev, wrap_callback(_event_handle))

        # ref
        if comp_ast.v_ref:
            _ref = ns.getattr(comp_ast.v_ref)
            if not isinstance(_ref, RefImpl):
                err_msg = f'v-ref={comp_ast.v_ref} needs to be of type Ref.'
                logger.error(err_msg)
                raise ValueError(err_msg)

            _ref.value = component if isinstance(component_cls, SFCType) else widget

        return widget

    # @staticmethod
    # def add_event_listener(widget, event, listener):
    #     listener = wrap_callback(listener)
    #     if hasattr(widget, SFC.ADD_EVENT_LISTENER_FN):  # SFC
    #         getattr(widget, SFC.ADD_EVENT_LISTENER_FN)(event, listener)
    #     elif event.startswith('update:'):  # anywidget, ipyw
    #         attr = event.split(':', 1)[1]
    #         from panel.widgets import Widget
    #         if isinstance(widget, Widget):
    #             widget.param.watch(listener, attr)
    #         else:
    #             widget.observe(listener, names=attr)
    #     else:  # ipyw click
    #         getattr(widget, f"on_{event}")(listener)


# todo move to backend
def wrap_callback(callback):
    """
    Wraps a callback function to handle coroutines.
    If the callback returns a coroutine, it will be scheduled to run in the event loop.
    If the callback returns a non-coroutine, it will be returned immediately.
    """
    def _callback(*args, **kwargs):
        ret = callback(*args, **kwargs)
        if isinstance(ret, Coroutine):
            # for jupyter
            loop = asyncio.get_event_loop()
            if loop.is_running():
                return asyncio.create_task(ret)
            else:
                asyncio.run(ret)
        return ret
    return _callback
