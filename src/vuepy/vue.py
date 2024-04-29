#!coding: utf-8
from __future__ import annotations
import abc
import ast
import dataclasses
from dataclasses import field
import enum
import importlib.util
import pathlib
import re
import types
from _ast import Attribute
from collections import defaultdict
from html.parser import HTMLParser
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import SupportsIndex
from typing import Type
from typing import Union

import ipywidgets as widgets
from IPython.display import clear_output
from IPython.display import display
from ipywidgets import CallbackDispatcher

from vuepy import log as logging

logger = logging.getLogger()


def get_block_content_from_sfc(sfc_file, block):
    with open(sfc_file) as f:
        blocks = re.findall(f'<{block}>(.*)</{block}>', f.read(), flags=re.S | re.I)
    return blocks


def get_script_py_block_content_from_sfc(sfc_file):
    with open(sfc_file) as f:
        match = re.search(
            fr'<script\s+lang=(["\'])py\1\s*>(?P<content>.*)</script>',
            f.read(),
            flags=re.S | re.I
        )

    if not match:
        return None

    return match.group('content')


def get_template_from_sfc(sfc_file):
    return get_block_content_from_sfc(sfc_file, 'template')[0]


def get_script_src_from_sfc(sfc_file):
    with open(sfc_file) as f:
        match = re.search(r"<script (.*?)src=(['\"])(?P<src>.*?)\2></script>", f.read())
        if not match:
            return None
        return match.group('src')


class WatcherBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def update(self):
        pass


class PubEnum(enum.Enum):
    PROPERTY = 'property'
    SETUP = 'setup'


# Map<target_id, Map<key, List<effect>>>
SUBS_MAP = {
    PubEnum.PROPERTY: {},
    PubEnum.SETUP: {},
}


def get_subscribers_for_property_by_id(target_id, key, pub=PubEnum.PROPERTY):
    subs_map = SUBS_MAP[pub]
    if target_id not in subs_map:
        subs_map[target_id] = {}

    if key not in subs_map[target_id]:
        subs_map[target_id][key] = []

    return subs_map[target_id][key]


def get_subscribers_for_property(target, key, pub=PubEnum.PROPERTY):
    return get_subscribers_for_property_by_id(id(target), key, pub)


def add_subscribers_for_property(target, key, sub: WatcherBase, pub=PubEnum.PROPERTY):
    effects = get_subscribers_for_property(target, key, pub)
    effects.append(sub)


def clear_subscribers_for_property(target, key, pub=PubEnum.PROPERTY):
    effects = get_subscribers_for_property(target, key, pub)
    effects.clear()


def trigger_subscribers_for_property(target, key):
    for pub in PubEnum:
        effects = get_subscribers_for_property(target, key, pub)
        for effect in effects:
            effect.update()
            if isinstance(effect, WatcherForRerender):
                return


g_active_effect = None
g_pub = None


def track(target, key):
    if not g_active_effect:
        return

    if g_pub:
        add_subscribers_for_property(target, key, g_active_effect, g_pub)
    else:
        add_subscribers_for_property(target, key, g_active_effect, PubEnum.PROPERTY)


def trigger(target, key):
    trigger_subscribers_for_property(target, key)


class ActivateEffect:
    def __init__(self, effect, pub=PubEnum.PROPERTY):
        self.effect = effect
        self.pub = pub

    def __enter__(self):
        global g_active_effect
        global g_pub
        g_active_effect = self.effect
        g_pub = self.pub

    def __exit__(self, exc_type, exc_val, exc_tb):
        global g_active_effect
        global g_pub
        g_active_effect = None
        g_pub = None


class Dep:
    def __init__(self):
        self.subs: List[WatcherBase] = []

    def add_sub(self, sub):
        if sub in self.subs:
            return

        self.subs.append(sub)

    def reset_subs(self):
        self.subs.clear()

    def notify(self):
        for sub in self.subs:
            sub.update()


class DepStoreField:
    _deps: Dict[int, Dict[str, Dep]] = {}

    def __init__(self):
        pass

    @classmethod
    def reset(cls):
        cls._deps = {}

    def __get__(self, instance, owner):
        instance_id = id(instance)
        if instance_id not in self._deps:
            self._deps[instance_id] = defaultdict(Dep)

        return self._deps[instance_id]

    def __set__(self, instance, new_value):
        pass

    def __delete__(self, instance):
        instance_id = id(instance)
        if instance_id in self._deps:
            del self._deps[instance_id]


class Reactive(metaclass=abc.ABCMeta):
    _deps = DepStoreField()

    @abc.abstractmethod
    def add_dep(self, attr, sub):
        pass

    @abc.abstractmethod
    def reset_deps(self):
        pass


class ReactiveDict(dict, Reactive):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, attr):
        track(self, attr)
        return super().__getitem__(attr)

    def __setitem__(self, attr, value):
        super().__setitem__(attr, value)
        trigger(self, attr)

    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __setattr__(self, attr, value):
        self.__setitem__(attr, value)

    def __delete__(self, instance):
        del self._deps

    def add_dep(self, attr, sub):
        self._deps[attr].add_sub(sub)

    def reset_deps(self):
        for k, v in self.items():
            clear_subscribers_for_property(self, k, PubEnum.PROPERTY)
            if isinstance(v, Reactive):
                v.reset_deps()


class ReactiveList(list, Reactive):
    _SUB_KEY = '__reactive_list_sub_key'

    def append(self, __object) -> None:
        super().append(__object)
        trigger(self, self._SUB_KEY)

    def extend(self, __iterable) -> None:
        super().extend(__iterable)
        trigger(self, self._SUB_KEY)

    def insert(self, __index: SupportsIndex, __object) -> None:
        super().insert(__index, __object)
        trigger(self, self._SUB_KEY)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        trigger(self, self._SUB_KEY)

    def sort(self, *, key: None = ..., reverse: bool = ...) -> None:
        super().sort(key=key, reverse=reverse)
        trigger(self, self._SUB_KEY)

    def reverse(self) -> None:
        super().reverse()
        trigger(self, self._SUB_KEY)

    def pop(self, __index: SupportsIndex = ...):
        ret = super().pop(__index)
        trigger(self, self._SUB_KEY)
        return ret

    def remove(self, __value) -> None:
        super().remove(__value)
        trigger(self, self._SUB_KEY)

    def __delete__(self, instance):
        del self._deps

    def add_dep(self, sub):
        add_subscribers_for_property(self, self._SUB_KEY, sub)

    def reset_deps(self):
        clear_subscribers_for_property(self, self._SUB_KEY, PubEnum.PROPERTY)
        for item in self:
            if isinstance(item, Reactive):
                item.reset_deps()


def observe(data):
    if isinstance(data, Reactive):
        data.reset_deps()

    if isinstance(data, dict):
        for attr, item in data.items():
            data[attr] = observe(item)
        if not isinstance(data, Reactive):
            data = ReactiveDict(data)

    elif isinstance(data, list):
        for i, item in enumerate(data):
            data[i] = observe(item)
        if not isinstance(data, Reactive):
            data = ReactiveList(data)

    return data


class VueRef(Reactive):
    _SUB_KEY = '__ref_sub_key'

    def __init__(self, value):
        super().__init__()
        self._value = value

    @property
    def value(self):
        track(self, self._SUB_KEY)
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        trigger(self, self._SUB_KEY)

    def add_dep(self, sub):
        add_subscribers_for_property(self, self._SUB_KEY, sub)

    def reset_deps(self):
        clear_subscribers_for_property(self, self._SUB_KEY, PubEnum.PROPERTY)
        if isinstance(self._value, Reactive):
            self._value.reset_deps()


def ref(value):
    return VueRef(value)


def reactive(obj):
    return observe(obj)


def computed(func, setter=None):
    val_ref = ref(None)
    watcher = WatcherForComputed(val_ref, func)
    with ActivateEffect(watcher, PubEnum.SETUP):
        val_ref.value = func()
    return val_ref


def watch(source, callback, options=None):
    def _watch_reactive_obj(data: Reactive, source, callback):
        if isinstance(data, dict):
            for attr, item in data.items():
                _watch_reactive_obj(item, source, callback)

        elif isinstance(data, list):
            for i, item in enumerate(data):
                _watch_reactive_obj(item, source, callback)

    options = options or {}
    watcher = WatcherForWatchFunc(source, callback, options)
    with ActivateEffect(watcher, PubEnum.SETUP):
        if isinstance(source, VueRef):
            _ = source.value
        elif isinstance(source, Reactive):
            _watch_reactive_obj(source, source, callback)
        elif callable(source):
            deep = options.get('deep', True)
            _ = source()


class WatcherForRerender(WatcherBase):
    def __init__(self, vm, name):
        self.vm = vm
        self.name = name

    def update(self):
        self.vm.render()


class WatcherForComputed(WatcherBase):
    def __init__(self, source, func, options=None):
        self.source = source
        self.func = func
        self.value = self.get_val()

    def get_val(self):
        return self.func()

    def update(self):
        old_val = self.value
        new_val = self.get_val()
        try:
            if new_val == self.value:
                return
        except Exception as e:
            pass

        self.value = new_val
        self.source.value = new_val


class WatcherForWatchFunc(WatcherBase):
    def __init__(self, source, callback, options=None):
        self.source = source
        self.callback = callback
        self.value = self.get_val()

    def get_val(self):
        if isinstance(self.source, VueRef):
            return self.source.value
        else:
            return self.source

    def update(self):
        old_val = self.value
        new_val = self.get_val()
        try:
            if new_val == self.value:
                return
        except Exception as e:
            pass

        self.value = new_val
        self.callback(new_val, old_val)


class WatcherForAttrUpdate(WatcherBase):
    def __init__(self, ns: "VueCompNamespace", val_expr_or_fn, callback, options=None):
        self.callback = callback
        self.val_expr_or_fn = val_expr_or_fn
        self.ns = ns
        self.value = self.get_val()

    def get_val(self):
        if callable(self.val_expr_or_fn):
            return self.val_expr_or_fn()
        else:
            return self.val_expr_or_fn.eval(self.ns)

    def update(self):
        new_val = self.get_val()
        old_val = self.value
        try:
            if new_val == old_val:
                return
        except Exception as e:
            pass

        self.value = new_val
        self.callback(new_val, old_val)


class VForStatement:
    def __init__(self, target, iters, index=None):
        self.i = index
        self.target = target
        self.iter = iters

    @classmethod
    def parse(cls, s):
        """
        (i, target) in iter
        :param s:
        :return:
        """
        i_target, iters = [i.strip() for i in s.split(' in ')]
        i_target = [i.strip() for i in i_target.strip('()').split(',')]
        if len(i_target) == 1:
            i, target = None, i_target[0]
        else:
            i, target = i_target[0], i_target[1]

        return cls(target.strip(), iters, i)


class ForScope:
    def __init__(self, i_val, for_stmt: VForStatement, vm: 'VueComponent'):
        self.for_stmt = for_stmt
        self.i = i_val
        self.iter = VueCompNamespace.get_by_attr_chain(vm._data, for_stmt.iter)
        self.target = self.iter[self.i]

    def to_ns(self):
        return {
            self.for_stmt.i: self.i,
            self.for_stmt.target: self.target,
            self.for_stmt.iter: self.iter,
        }


class VueCompExprAst:
    def __init__(self, exp_ast, vars=None, exp_str=''):
        self.vars = vars if vars else []
        self.exp_ast = exp_ast
        self.exp_str = exp_str

    def add_var(self, var):
        self.vars.append(var)

    def eval(self, ns, local_vars=None):
        return vue_comp_expr_eval(self, ns, local_vars)


class VueCompExprParser:
    @staticmethod
    def parse(exp_str) -> ast.Expression:
        return ast.parse(exp_str, mode='eval')


class VueCompExprTransformer(ast.NodeTransformer):
    def __init__(self):
        self.vars = []
        self._in_attr = False

    @classmethod
    def get_attr_chain(cls, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            base = cls.get_attr_chain(node.value)
            return f"{base}.{node.attr}"

    def visit_Attribute(self, node: Attribute) -> Any:
        if self._in_attr:
            return node

        self._in_attr = True
        self.vars.append(self.get_attr_chain(node))

        self.generic_visit(node)
        self._in_attr = False
        return node

    def transformer(self, exp_ast: ast.Expression):
        if isinstance(exp_ast.body, ast.Name):
            self.vars = [exp_ast.body.id]
        else:
            self.visit(exp_ast)

        return VueCompExprAst(exp_ast, self.vars)


def vue_comp_expr_parse(expr_str):
    _ast = VueCompExprParser.parse(expr_str)
    transformer = VueCompExprTransformer()
    comp_expr_ast = transformer.transformer(_ast)
    comp_expr_ast.exp_str = expr_str
    return comp_expr_ast


def vue_comp_expr_compile(expr_ast: VueCompExprAst):
    return compile(expr_ast.exp_ast, "<string>", "eval")


def vue_comp_expr_eval(expr_ast: VueCompExprAst, ns: "VueCompNamespace", local_vars=None):
    code_obj = expr_ast if isinstance(expr_ast, types.CodeType) else vue_comp_expr_compile(expr_ast)
    return eval(code_obj, {"__builtin__": None}, ns.to_py_eval_ns(local_vars))


class VueCompAst:
    V_IF = 'v-if'
    V_FOR = 'v-for'
    V_SLOT = 'v-slot:'
    V_SLOT_ABBR = '#'
    V_JS_LINK = 'v-js-link'
    V_REF = 'ref'
    V_MODEL = 'v-model:'
    V_MODEL_DEFAULT = 'v-model'
    V_HTML = 'v-html'
    V_ON = 'v-on:'
    V_ON_ABBR = '@'
    V_BIND = 'v-bind:'
    V_BIND_ABBR = ':'

    LAYOUT_ATTRS = {'width', 'height', 'padding', 'border'}

    # todo 和h函数的参数保持一致
    def __init__(self, tag):
        self.tag = tag
        self.v_if: VueCompExprAst = None
        # todo rename to attrs
        self.kwargs = {}
        self.v_binds: Dict[str, VueCompExprAst] = {}
        # todo support only one v-model
        self.v_model: List[(str, str)] = []
        self.v_html = None
        self.v_on: Dict[str, VueCompExprAst] = {}
        self.layout = {}
        self.v_slot = None
        self.v_ref = None

    @classmethod
    def is_v_if(cls, attr):
        return attr == cls.V_IF

    @classmethod
    def is_v_slot(cls, attr):
        return attr.startswith(cls.V_SLOT)

    @classmethod
    def is_v_slot_addr(cls, attr):
        return attr.startswith(cls.V_SLOT_ABBR)

    @classmethod
    def is_v_ref(cls, attr):
        return attr == cls.V_REF

    @classmethod
    def is_v_model_default(cls, attr):
        return attr == cls.V_MODEL_DEFAULT

    @classmethod
    def is_v_model(cls, attr):
        return attr.startswith(cls.V_MODEL)

    @classmethod
    def is_v_html(cls, attr):
        return attr == cls.V_HTML

    @classmethod
    def is_v_on(cls, attr):
        return attr.startswith(cls.V_ON)

    @classmethod
    def is_v_on_abbr(cls, attr):
        return attr.startswith(cls.V_ON_ABBR)

    @classmethod
    def is_v_bind(cls, attr):
        return attr.startswith(cls.V_BIND)

    @classmethod
    def is_v_bind_abbr(cls, attr):
        return attr.startswith(cls.V_BIND_ABBR)

    @classmethod
    def is_layout(cls, attr):
        return attr in cls.LAYOUT_ATTRS

    @classmethod
    def parse(cls, tag, attr_dict):
        comp = cls(tag)
        for attr, value in attr_dict.items():
            if cls.is_v_if(attr):
                comp.v_if = vue_comp_expr_parse(value)

            elif cls.is_v_bind(attr):
                attr = attr.split(cls.V_BIND, 1)[1]
                comp.v_binds[attr] = vue_comp_expr_parse(value)

            elif cls.is_v_bind_abbr(attr):
                attr = attr.split(cls.V_BIND_ABBR, 1)[1]
                comp.v_binds[attr] = vue_comp_expr_parse(value)

            elif cls.is_v_model_default(attr):
                comp.v_model.append((defineModel.DEFAULT_KEY, value))

            elif cls.is_v_model(attr):
                _define_model_key = attr.split(cls.V_MODEL, 1)[1]
                comp.v_model.append((_define_model_key, value))

            elif cls.is_v_html(attr):
                comp.v_html = value

            elif cls.is_v_on(attr) or cls.is_v_on_abbr(attr):
                _prefix = cls.V_ON if cls.is_v_on(attr) else cls.V_ON_ABBR
                event = attr.split(_prefix, 1)[1]
                func_ast = vue_comp_expr_parse(value)
                if isinstance(func_ast.exp_ast.body, (ast.Name, ast.Attribute)):
                    exp_ast = ast.Expression(
                        ast.Call(func=func_ast.exp_ast.body,
                                 args=[ast.Name(id='__owner', ctx=ast.Load())],
                                 keywords=[])
                    )
                    ast.fix_missing_locations(exp_ast)
                    func_ast.exp_ast = exp_ast

                comp.v_on[event] = func_ast

            elif tag == 'template' and cls.is_v_slot(attr):
                comp.v_slot = attr.split(cls.V_SLOT, 1)[1]

            elif tag == 'template' and cls.is_v_slot_addr(attr):
                comp.v_slot = attr.split(cls.V_SLOT_ABBR, 1)[1]

            elif cls.is_v_ref(attr):
                comp.v_ref = value

            elif cls.is_layout(attr):
                comp.layout[attr] = value

            else:
                comp.kwargs[attr] = value

        if comp.layout:
            comp.kwargs['layout'] = comp.layout

        return comp


class Nil:
    pass


class VueCompNamespace:
    def __init__(self, root, global_vars, local_vars=None):
        self.local_vars = local_vars or {}
        self.global_vars = global_vars
        self.root = root
        self.ns_list = [
            self.local_vars,
            self.global_vars,
        ]

    def to_py_eval_ns(self, tmp_vars=None):
        return {
            **self.global_vars,
            **self.local_vars,
            **(tmp_vars or {}),
        }

    @staticmethod
    def _getattr(obj, attr, default=Nil):
        if isinstance(obj, dict):
            return obj[attr] if default is Nil else obj.get(attr, default)
        else:
            return getattr(obj, attr) if default is Nil else getattr(obj, attr, default)

    @classmethod
    def get_by_attr_chain(cls, obj, attr_chain, default=Nil):
        for attr in attr_chain.split('.'):
            obj = cls._getattr(obj, attr, Nil)
            if obj is Nil:
                break
        else:
            return obj

        raise Exception(f"get attr {attr_chain} from ns failed")

    def get_obj_and_attr(self, attr_chain):
        obj_attr_tuple = attr_chain.rsplit('.', 1)
        for ns in self.ns_list:
            if not ns:
                continue

            if len(obj_attr_tuple) == 1:
                if attr_chain not in ns:
                    continue
                else:
                    return self.root, attr_chain

            obj_attr_chain, attr = obj_attr_tuple
            obj = self.get_by_attr_chain(ns, obj_attr_chain)
            if obj is not Nil:
                return obj, attr

        raise Exception(f"get attr {attr_chain} from ns failed")

    def getattr(self, attr_chain, default=Nil):
        return self.get_by_attr_chain(self.to_py_eval_ns(), attr_chain, default)


class VueCompCodeGen:
    """
    h()
    """
    @staticmethod
    def handle_value_change_vm_to_view(widget, attr):
        def warp(val, old_val):
            try:
                if val == old_val:
                    return
            except Exception as e:
                pass
            setattr(widget, attr, val)
        return warp

    @classmethod
    def gen(cls, comp_ast: VueCompAst, children, vm: 'VueComponent', ns: VueCompNamespace, app: App):
        component_cls: Type[VueComponent] = vm.component(comp_ast.tag)
        # v-if
        if comp_ast.v_if:
            watcher = WatcherForRerender(vm, f'v_if {comp_ast.v_if}')
            with ActivateEffect(watcher):
                if not comp_ast.v_if.eval(ns):
                    return widgets.HTML("")

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
        # if comp_ast.v_model:
        #     props.update({
        #         _model_key: ns.getattr(_bind) for _model_key, _bind in comp_ast.v_model
        #     })

        if isinstance(component_cls, SFCFactory):
            component = component_cls(props, ctx, app)
        else:
            component = component_cls()
        widget = component.render(ctx, props, {})

        # v-slot
        if comp_ast.v_slot:
            widget.v_slot = comp_ast.v_slot

        # v-bind:
        for widget_attr, exp_ast in comp_ast.v_binds.items():
            update_vm_to_view = cls.handle_value_change_vm_to_view(widget, widget_attr)
            watcher = WatcherForAttrUpdate(ns, exp_ast, update_vm_to_view)
            with ActivateEffect(watcher):
                _value = exp_ast.eval(ns)
            update_vm_to_view(_value, None)

        # v-model:define-model=bind
        for _model_key, attr_chain in comp_ast.v_model:
            # :bind, parent to child
            # widget_attr = component_cls.v_model_default  # VueCompTag.v_model(comp_ast.tag)
            widget_attr = _model_key
            if _model_key == defineModel.DEFAULT_KEY and hasattr(component_cls, 'v_model_default'):
                widget_attr = getattr(component_cls, 'v_model_default')

            update_vm_to_view = cls.handle_value_change_vm_to_view(widget, widget_attr)
            watcher = WatcherForAttrUpdate(ns, lambda: ns.getattr(attr_chain), update_vm_to_view)
            with ActivateEffect(watcher):
                _value = ns.getattr(attr_chain)
            update_vm_to_view(_value, None)

            # v-on, child to parent
            def listener(obj, attr):
                def _(change):
                    val = change['new']
                    setattr(obj, attr, val)
                    if isinstance(obj, defineModel) and isinstance(widget, SFCWidgetContainer):
                        getattr(widget, SFC.EMIT_FN)(obj.update_event, val)
                return _

            obj, attr = ns.get_obj_and_attr(attr_chain)
            add_event_listener(
                widget,
                f'update:{_model_key}',
                listener(obj, attr),
            )

        # v-on
        for ev, func_ast in comp_ast.v_on.items():
            add_event_listener(
                widget, ev,
                lambda payload, _func_ast=func_ast: _func_ast.eval(ns, {'__owner': payload})
            )

        if comp_ast.v_ref:
            _ref = ns.getattr(comp_ast.v_ref)
            if not isinstance(_ref, VueRef):
                logger.error(f'ref={comp_ast.v_ref} is not instance of VueRef.')
            else:
                _ref.value = widget

        return widget


def add_event_listener(widget, event, listener):
    if hasattr(widget, SFC.ADD_EVENT_LISTENER_FN):  # SFC
        getattr(widget, SFC.ADD_EVENT_LISTENER_FN)(event, listener)
    elif event.startswith('update:'):  # anywidget, ipyw
        attr = event.split(':', 1)[1]
        widget.observe(listener, names=attr)
    else:  # ipyw click
        getattr(widget, f"on_{event}")(listener)


class VueCompHtmlTemplateRender:
    @staticmethod
    def replace(vm: "VueComponent", ns: VueCompNamespace, for_idx):
        def warp(match):
            exp = match.group(1)
            exp_ast = vue_comp_expr_parse(exp)
            # TODO html可以设置value，按需更新
            watcher = WatcherForRerender(vm, f'html {for_idx} {{{{ {exp} }}}}')
            with ActivateEffect(watcher):
                _value = exp_ast.eval(ns)
            return str(_value)
        return warp

    @classmethod
    def render(cls, template, vm: 'VueComponent', ns: VueCompNamespace, for_idx=-1):
        exp_pattern = r"\{\{\s*(.*?)\s*\}\}"
        result = re.sub(exp_pattern, cls.replace(vm, ns, for_idx), template)
        return result


class DomCompiler(HTMLParser):
    """
    @vue/compiler-dom

    数据绑定:
    https://docs.python.org/zh-cn/3.10/library/ast.html#function-and-class-definitions
    https://juejin.cn/post/7242700247440293925
    https://www.chuchur.com/article/vue-mvvm-complie
    https://github.com/leilux/SICP-exercises/blob/master/book/p216-constraint-propagate(python%20version).py
    """

    def __init__(self, vm: VueComponent, app: 'App'):
        super().__init__()
        self.vm = vm
        self.app = app
        self.widgets = []
        self.widgets_by_id = {}
        self.parent_node_stack = []
        self.v_for_stack = []
        self.html_tags = []

    def _get_element_by_id(self, el_id):
        return self.widgets_by_id.get(el_id)

    @property
    def is_in_for_stmt(self):
        return bool(self.v_for_stack)

    def _process_directive(self):
        pass

    def _gen_ast_node(self, tag, attrs, for_scope=None):
        if self.vm.component(tag):
            node = self._component_tag_enter(tag, attrs, for_scope)
        else:
            node = self._html_tag_enter(tag, attrs)
        return node

    def _gen_widget(self, node, for_scope=None):
        tag = node['tag']
        if self.vm.component(tag):
            widget = self._component_tag_exit(node, for_scope)
        else:
            widget = self._html_tag_exit(node, for_scope)

        return widget

    def _component_tag_enter(self, tag, attrs, for_scope=None):
        return {"tag": tag, 'attrs': attrs, 'body': []}

    def _component_tag_exit(self, node, for_scope=None):
        comp_ast = VueCompAst.parse(node['tag'], node['attrs'])
        local = for_scope.to_ns() if for_scope else None
        ns = VueCompNamespace(self.vm._data, self.vm.to_ns(), local)
        widget = VueCompCodeGen.gen(comp_ast, node['body'], self.vm, ns, self.app)
        return widget

    def _html_tag_enter(self, tag, attrs):
        ast_node = {'type': 'html', 'tag': tag, 'attrs': attrs, 'body': []}
        return ast_node

    def _html_tag_exit(self, node, for_scope: ForScope = None):
        # TODO 重构
        comp_ast = VueCompAst.parse(node['tag'], node['attrs'])
        local = for_scope.to_ns() if for_scope else None
        ns = VueCompNamespace(self.vm._data, self.vm.to_ns(), local)
        # v-if
        widget = widgets.HTML("")
        if comp_ast.v_if:
            watcher = WatcherForRerender(self.vm, f'v_if {comp_ast.v_if}')
            with ActivateEffect(watcher):
                if not comp_ast.v_if.eval(ns):
                    return widget

        tag = node['tag']
        attr = ' '.join([f"{k}='{v}'" for k, v in node['attrs'].items()])
        html_temp = f"<{tag} {attr}>{{inner_html}}</{tag}>"

        def gen_html(inner_html):
            return html_temp.format(inner_html=inner_html)

        def handle_value_change_vm_to_view(widget, attr):
            def warp(val, old_val):
                if val == old_val:
                    return
                setattr(widget, attr, gen_html(val))
            return warp

        # v-html
        if comp_ast.v_html:
            attr_chain = comp_ast.v_html
            update_vm_to_view = handle_value_change_vm_to_view(widget, 'value')
            watcher = WatcherForAttrUpdate(ns, lambda: ns.getattr(attr_chain), update_vm_to_view)
            with ActivateEffect(watcher):
                _value = ns.getattr(attr_chain)
            update_vm_to_view(_value, None)
        else:
            body = [
                child.value if isinstance(child, widgets.HTML) else child
                for child in node['body']
            ]
            widget.value = gen_html(' '.join(body))

        return widget

    def _for_stmt_enter(self, for_stmt: VForStatement, tag, attrs, is_body):
        body = []
        _iter = VueCompNamespace.get_by_attr_chain(self.vm._data, for_stmt.iter)
        for i, target in enumerate(_iter):
            for_scope = (i, target)
            body.append(self._gen_ast_node(tag, attrs, for_scope))

        if is_body:
            ast_node = {
                "tag": 'v_for',
                'v_for_body': for_stmt,
                "body": body,
            }
        else:
            ast_node = {
                "tag": 'v_for',
                'v_for': for_stmt,
                "body": body,
            }
        return ast_node

    def _for_stmt_exit(self, v_for_ast_node, is_body=False):
        _widgets = []
        v_for_stmt = self.v_for_stack[-1]
        _iter = VueCompNamespace.get_by_attr_chain(self.vm._data, v_for_stmt.iter)
        for i, target in enumerate(_iter):
            for_scope = ForScope(i, v_for_stmt, self.vm)
            node = v_for_ast_node['body'][i]
            widget = self._gen_widget(node, for_scope)
            if widget:
                _widgets.append(widget)

        # todo 加到v-for的解析处
        if not is_body:
            ns = VueCompNamespace(self.vm._data, self.vm.to_ns())
            # 处理list被整个替换的情况
            attr_chain = v_for_stmt.iter
            _attrs = attr_chain.split('.', 1)
            if len(_attrs) > 1:
                base_attr, sub_attr_chain = _attrs
                obj = ns.getattr(base_attr)
                watcher = WatcherForRerender(self.vm, f"for_stme {v_for_stmt.iter} replace")
                with ActivateEffect(watcher):
                    VueCompNamespace.get_by_attr_chain(obj, sub_attr_chain)
            # 处理list本身的变化，append、pop等操作
            # watcher = WatcherForRerender(self.vm, f"{v_for_stmt.iter} modified")
            # with ActivateEffect(watcher):
            obj_iter = ns.getattr(v_for_stmt.iter)
            if isinstance(obj_iter, Reactive):
                obj_iter.add_dep(WatcherForRerender(self.vm, f"{v_for_stmt.iter} modified"))

        return _widgets

    def _get_raw_tag(self, tag):
        row, col = self.getpos()
        row_idx = row - 1
        col_idx = col + 1
        return self.html_lines[row_idx][col_idx: col_idx + len(tag)]

    def _to_camel_case_tag(self, tag):
        words = tag.split('-')
        if len(words) == 1:
            return tag
        return ''.join(w.title() for w in words)

    def handle_starttag(self, case_insensitive_tag, attrs):
        raw_tag = self._get_raw_tag(case_insensitive_tag)
        tag = self._to_camel_case_tag(raw_tag)

        attrs = dict(attrs)
        v_for_stmt = attrs.pop(VueCompAst.V_FOR, None)
        if v_for_stmt or self.v_for_stack:
            is_header = bool(v_for_stmt)
            if is_header:
                v_for = VForStatement.parse(v_for_stmt)
                self.v_for_stack.append(v_for)
            v_for = self.v_for_stack[-1]
            node = self._for_stmt_enter(v_for, tag, attrs, not is_header)
        else:
            node = self._gen_ast_node(tag, attrs)
        self.parent_node_stack.append(node)

    def handle_data(self, data: str) -> None:
        if not self.parent_node_stack:
            return

        parent = self.parent_node_stack[-1]
        if not self.is_in_for_stmt:
            if parent.get('type') != 'html':
                return

            ns = VueCompNamespace(self.vm._data, self.vm.to_ns())
            result = VueCompHtmlTemplateRender.render(data, self.vm, ns, -1)
            parent['body'].append(result)

        # TODO node的类型判断可以优化
        elif parent['body'] and parent['body'][0].get('type') == 'html':
            v_for_stmt = self.v_for_stack[-1]
            _iter = VueCompNamespace.get_by_attr_chain(self.vm._data, v_for_stmt.iter)
            for i, target in enumerate(_iter):
                for_scope = ForScope(i, v_for_stmt, self.vm)
                ns = VueCompNamespace(self.vm._data, self.vm.to_ns(), for_scope.to_ns())
                result = VueCompHtmlTemplateRender.render(data, self.vm, ns, i)
                parent['body'][i]['body'].append(result)

    def handle_endtag(self, tag):
        node = self.parent_node_stack.pop()
        if self.is_in_for_stmt:
            is_body = 'v_for' not in node
            _widgets = self._for_stmt_exit(node, is_body)
            if is_body:
                for i, widget in enumerate(_widgets):
                    self.parent_node_stack[-1]['body'][i]['body'].append(widget)
            else:
                self.parent_node_stack[-1]['body'].extend(_widgets)
                self.v_for_stack.pop()
        else:
            widget = self._gen_widget(node)
            if not widget:
                return

            if self.parent_node_stack:
                self.parent_node_stack[-1]['body'].append(widget)
            else:
                self.widgets.append(widget)

    def compile(self, html):
        self.html_lines = [line for line in html.splitlines()]
        self.feed(html)
        if len(self.widgets) == 1:
            return self.widgets[0]
        return widgets.VBox(self.widgets)


class ScriptCompiler:
    @staticmethod
    def compile_script_block(code_str):
        module = ast.parse(code_str)
        func_name = 'setup'
        func_ast = ast.FunctionDef(
            name=func_name,
            args=ast.arguments(
                posonlyargs=[],
                args=[
                    ast.arg(arg='props', annotation=None),
                    ast.arg(arg='ctx', annotation=None),
                    ast.arg(arg='vm', annotation=None)
                ],
                vararg=None,
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None,
                defaults=[],
            ),
            body=module.body + [ast.parse('return locals()').body[0]],
            decorator_list=[],
            returns=None
        )

        module.body = [func_ast]
        ast.fix_missing_locations(module)
        code = compile(module, filename='<ast>', mode='exec')

        local_vars = {}
        exec(code, {}, local_vars)
        return local_vars[func_name]

    @staticmethod
    def compile_script_src(dir_path, src):
        _script_path = dir_path.joinpath(src)
        if not _script_path.exists():
            raise ValueError(f"sfc script {_script_path} not exists.")

        _spec = importlib.util.spec_from_file_location('sfc', str(_script_path))
        _module = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_module)
        return getattr(_module, 'setup')

    @classmethod
    def compile(cls, sfc_file):
        sfc_file = pathlib.Path(sfc_file)
        script_src = get_script_src_from_sfc(sfc_file)
        if script_src:
            return cls.compile_script_src(sfc_file.parent, script_src)
        else:
            script_block = get_script_py_block_content_from_sfc(sfc_file)
            return cls.compile_script_block(script_block)


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


class Document(widgets.VBox):
    """
    https://developer.mozilla.org/en-US/docs/Web/API/Document
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body = Dom()
        self.children = (self.body,)


@dataclasses.dataclass
class CompilerOptions:
    whitespace = 'condense'  # 'preserve'
    delimiters: List[str] = field(default_factory=lambda: ['{{', '}}'])
    comments: bool = False

    def is_custom_element(self, tag: str) -> bool:
        """
        用于指定一个检查方法来识别原生自定义元素。

        :param tag:
        :return:
        """
        pass


@dataclasses.dataclass
class AppConfig:
    """应用的配置设定"""
    # error_handler: ErrorHandler
    # warn_handler: WarningHandler
    # option_merge_strategies: dict[str, OptionMergeFunction] = {}
    global_properties: dict[str, Any] = field(default_factory=dict)
    compiler_options: CompilerOptions = CompilerOptions()
    performance: bool = False


class Directive:
    pass


@dataclasses.dataclass
class AppContext:
    app: 'App'
    config: AppConfig
    directives: dict[str, Directive]
    provides: dict[str, Any]
    components: dict[str, VueComponent] = field(default_factory=dict)


class SetupContext:
    def __init__(self):
        self.attrs = {}
        self.slots = {}
        # 触发事件
        self.emit = {}
        # 暴露公共属性
        self.expose = {}


@dataclasses.dataclass
class VueOptions:
    # (props: dict, context: SetupContext, app: App) -> dict | Callable[[], h]:
    setup: Callable[[dict, SetupContext | dict, 'App'], dict | Callable]
    template: str = ''
    # (self, ctx, props, setup_returned) -> VNode:
    render: Callable[[SetupContext | dict, dict, dict], VNode] = None

    def gen_component(self, props: dict, context: SetupContext, app: App) -> SFC:
        template_path = pathlib.Path(self.template)
        if template_path.exists():
            template = get_template_from_sfc(template_path)
        else:
            template = self.template

        sfc_factory = SFCFactory(
            setup=self.setup,
            template=template,
            _file='',
        )
        sfc = sfc_factory(props, context, app)
        return sfc


class App:
    components = {}

    def __init__(self, root_component: RootComponent, debug=False):
        self.version = ''
        self.config: AppConfig = AppConfig()

        self._installed_plugins = []
        self._props: dict = {}
        self._container = None
        self._context: AppContext = AppContext(self, self.config, {}, {})
        self._instance: VueComponent = None

        if isinstance(root_component, dict):
            root_component = VueOptions(**root_component)

        props = {}
        context = {}
        if isinstance(root_component, SFCFactory):
            self.root_component: SFC = root_component(props, context, self)
        elif isinstance(root_component, VueOptions):
            self.root_component: SFC = root_component.gen_component(props, context, self)
        else:
            raise ValueError(
                f"root_component only support {RootComponent}, {type(root_component)} found."
            )
        self.debug = debug

        self._components = {}

        self.document: Document = Document()
        self.dom = None

        self._proxy_methods()

    def _call_if_callable(self, func):
        if callable(func):
            func(self)

    # def __getattr__(self, key):
    #     if key == '_data':
    #         return super().__getattribute__(key)
    #
    #     if key in self._data:
    #         return self._data[key]
    #
    #     return super().__getattribute__(key)
    #
    # def __setattr__(self, key, value):
    #     if key == '_data':
    #         return super().__setattr__(key, value)
    #
    #     if key in self._data:
    #         self._data[key] = value
    #         return
    #     return super().__setattr__(key, value)

    def _proxy_methods(self):
        pass

    def render(self):
        if not isinstance(self.root_component, SFC):
            raise ValueError(f"render failed, root_component type {type(self.root_component)}.")

        # self.dom = self.options.render({}, self._props, self._data)
        self.dom = self.root_component.render()
        # with self.options.el:
        with self._container:
            clear_output(True)
            display(self.dom)

    def component(self, name: str, comp: 'VueComponent' = None):
        """
        query component(name) -> Component | None
        register component(name, comp) -> self

        :param name:
        :param comp:
        :return:
        """
        # query
        if comp is None:
            return self._components.get(name, self.components.get(name, None))

        # register
        self._components[name] = comp
        return self

    def directive(self, name: str, directive: Directive = None) -> Directive | "App":
        """
        query directive(name) -> Directive | None
        register directive(name) -> self

        :param name:
        :param directive:
        :return:
        """
        pass

    def use(self, plugin: Type["VuePlugin"], options: dict = None):
        """
        install plugin.

        :param plugin: 插件本身
        :param options: 要传递给插件的选项
        :return:
        """
        if plugin in self._installed_plugins:
            return self

        plugin.install(self, options)
        return self

    def mount(self, el=None):
        self._container = el or widgets.Output()
        # self._call_if_callable(self.options.before_mount)
        self.render()
        # self._call_if_callable(self.options.mounted)
        self.document.body.appendChild(self._container)
        return self.document


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

    def setup(self, props: dict = None, ctx=None, vm: App = None):
        """

        :param props:
        :param ctx: attrs, slots, emit
        :param vm:
        :return:
        """
        pass

    def component(self, name: str):
        comp = self._data.get(name)
        try:
            if comp and (
                    isinstance(comp, SFCFactory)
                    or issubclass(comp, VueComponent)
            ):
                return comp
        except Exception as e:
            logger.warn(f"find component({name}) in Component `{self.name()}` failed, {e}.")
            pass

        comp = self.app.component(name)
        if comp is None:
            logger.warn(f"component({name}) not found in Component `{self.name()}`.")

        return comp

    def to_ns(self):
        return self._data

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

#
# def create_vnode(component: VueComponent, props):
#     """
#     https://cn.vuejs.org/guide/extras/render-function.html#render-function-recipes
#     h函数实际就是接受了一个component的ast表示
#     h(tag, props | attrs, children) => vnode
#
#     :param component:
#     :param props:
#     :return:
#     """
#     pass
#
#
# def create_element_vnode(tag, props):
#     pass
#
#
# def create_element_block():
#     pass
#
#
# def render_slot():
#     pass


class VuePlugin:
    @classmethod
    @abc.abstractmethod
    def install(cls, app: App, options: dict):
        pass


class DefineProp:
    def __init__(self, prop_name, default=None):
        self.name = prop_name
        self._value = ref(default)

    @property
    def value(self):
        return self._value.value

    @value.setter
    def value(self, val):
        self._value.value = val


class defineProps:
    """
    props = defineProps('p1')
    props.p1.value
    """

    def __init__(self, props: dict | list):
        self.prop_names = props
        self.props: List[DefineProp] = [DefineProp(name) for name in self.prop_names]
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

    def __call__(self, event, payload=None):
        """$emit event.

        :param event:
        :param payload:
        :return:
        """
        handlers = self.events_to_cb_dispatcher.get(event)
        if not handlers:
            raise Exception(f"Event {event} not supported.")
        handlers(payload)


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
        self.prop.value = val


class SFCWidgetContainer(Dom):
    pass


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
        self.root = _sfc_container()
        self._init_static_props(context.get('attrs', {}))

    def _init_static_props(self, attrs):
        if not self.define_props:
            return

        _, _props = self.define_props
        for prop_name in _props.prop_names:
            val = attrs.get(prop_name, Nil)
            if val is Nil:
                continue
            setattr(self.root, prop_name, val)

    def setup(self, props: dict = None, ctx=None, vm: App = None):
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
    def define_props(self) -> (str, defineProps):
        ret = self._get_define_x(defineProps, limit=1)
        return ret[0] if ret else []

    @property
    def define_emits(self) -> (str, defineEmits):
        ret = self._get_define_x(defineEmits, limit=1)
        return ret[0] if ret else []

    @property
    def define_models(self) -> List[(str, defineModel)]:
        return self._get_define_x(defineModel)

    def _get_define_x(self, define_type, limit: int = float('inf')):
        ret = []
        count = 0
        for var_name, var in self.setup_returned.items():
            if count >= limit:
                break
            if isinstance(var, define_type):
                ret.append([var_name, var])
                count += 1
        return ret

    def clear_property_subs(self):
        for item in self._data.values():
            if isinstance(item, Reactive):
                item.reset_deps()

    def render(self, ctx: SetupContext = None, props: dict = None, setup_returned: dict = None) -> VNode:
        self.clear_property_subs()
        if self._render:
            dom = self._render(self._context, self._props, self.setup_returned)
        else:
            dom = DomCompiler(self, self.app).compile(self.template)
        self.root.children = [dom]

        return self.root


@dataclasses.dataclass
class SFCFactory:
    # (props: dict, context: SetupContext, vm: App) -> dict | Callable[[], h]:
    setup: Callable[[dict, SetupContext | dict, 'App'], dict | Callable]
    template: str = ''
    # (self, ctx, props, setup_returned) -> VNode:
    render: Callable[[SetupContext | dict, dict, dict], VNode] = None
    _file: str = ''

    def __call__(self, props: dict, context: SetupContext | dict, app: App) -> "SFC":
        setup_ret = self.setup(props, context, app)
        return SFC(context, props, setup_ret, self.template, app, self.render)


def compile_script_block_setup(s):
    module = ast.parse(s)
    func_name = 'setup'
    func_ast = ast.FunctionDef(
        name=func_name,
        args=ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(arg='props', annotation=None),
                ast.arg(arg='ctx', annotation=None),
                ast.arg(arg='vm', annotation=None)
            ],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[],
        ),
        body=module.body + [ast.parse('return locals()').body[0]],
        decorator_list=[],
        returns=None
    )

    module.body = [func_ast]
    ast.fix_missing_locations(module)
    code = compile(module, filename='<ast>', mode='exec')

    local_vars = {}
    exec(code, {}, local_vars)
    return local_vars[func_name]


def import_sfc(sfc_file):
    sfc_file = pathlib.Path(sfc_file)
    setup = ScriptCompiler.compile(sfc_file)

    return SFCFactory(**{
        'setup': setup,
        'template': get_template_from_sfc(sfc_file),
        '_file': sfc_file,
    })


RootComponent = Type[Union[Type[VueComponent], SFCFactory, dict]]


def create_app(root_component: RootComponent, **root_props) -> App:
    """创建一个应用实例
    app = create_app(App)
    app = create_app({})

    :param root_component:
    :param root_props:
    :return:
    """
    debug = root_props.get('debug', False)
    return App(root_component, debug)
