#!coding: utf-8
from __future__ import annotations

import abc
import ast
import dataclasses
import enum
import functools
import importlib.util
import inspect
import pathlib
import re
import types
from _ast import Attribute
from _ast import Load
from _ast import Name
from _ast import Starred
from _ast import keyword
from dataclasses import field
from html.parser import HTMLParser
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple
from typing import Type
from typing import Union

import ipywidgets as widgets
from IPython.display import clear_output
from IPython.display import display
from ipywidgets import CallbackDispatcher

from vuepy import log as logging
from vuepy.reactivity.effect_scope import EffectScope
from vuepy.reactivity.reactive import to_raw
from vuepy.reactivity.ref import RefImpl
from vuepy.reactivity.ref import ref
from vuepy.reactivity.watch import WatchOptions
from vuepy.reactivity.watch import watch
from vuepy.utils.common import has_changed

logger = logging.getLogger()


# def get_block_content_from_sfc(sfc_file, block):
#     with open(sfc_file) as f:
#         blocks = re.findall(f'<{block}>(.*)</{block}>', f.read(), flags=re.S | re.I)
#     return blocks
#
#
# def get_script_py_block_content_from_sfc(sfc_file):
#     with open(sfc_file) as f:
#         match = re.search(
#             fr'<script\s+lang=(["\'])py\1\s*>(?P<content>.*)?</script>',
#             f.read(),
#             flags=re.S | re.I
#         )
#
#     if not match:
#         logger.debug("can't find <script lang=py>")
#         return None
#
#     return match.group('content')
#
#
# def get_template_from_sfc(sfc_file):
#     return get_block_content_from_sfc(sfc_file, 'template')[0]
#
#
# def get_script_src_from_sfc(sfc_file):
#     with open(sfc_file) as f:
#         match = re.search(r"<script (.*?)src=(['\"])(?P<src>.*?)\2></script>", f.read())
#         if not match:
#             return None
#         return match.group('src')


# class WatcherBase(metaclass=abc.ABCMeta):
#     @abc.abstractmethod
#     def update(self):
#         pass
#
#
# class PubEnum(enum.Enum):
#     PROPERTY = 'property'
#     SETUP = 'setup'
#
#
# # Map<target_id, Map<key, List<effect>>>
# SUBS_MAP = {
#     PubEnum.PROPERTY: {},
#     PubEnum.SETUP: {},
# }
#
#
# def get_subscribers_for_property_by_id(target_id, key, pub=PubEnum.PROPERTY):
#     subs_map = SUBS_MAP[pub]
#     if target_id not in subs_map:
#         subs_map[target_id] = {}
#
#     if key not in subs_map[target_id]:
#         subs_map[target_id][key] = []
#
#     return subs_map[target_id][key]
#
#
# def get_subscribers_for_property(target, key, pub=PubEnum.PROPERTY):
#     return get_subscribers_for_property_by_id(id(target), key, pub)
#
#
# def add_subscribers_for_property(target, key, sub: WatcherBase, pub=PubEnum.PROPERTY):
#     effects = get_subscribers_for_property(target, key, pub)
#     effects.append(sub)
#
#
# def clear_subscribers_for_property(target, key, pub=PubEnum.PROPERTY):
#     effects = get_subscribers_for_property(target, key, pub)
#     effects.clear()
#
#
# def trigger_subscribers_for_property(target, key):
#     for pub in PubEnum:
#         effects = get_subscribers_for_property(target, key, pub)
#         for effect in effects:
#             effect.update()
#             if isinstance(effect, WatcherForRerender):
#                 return
#
#
# g_active_effect = None
# g_pub = None
#
#
# def track(target, key):
#     if not g_active_effect:
#         return
#
#     if g_pub:
#         add_subscribers_for_property(target, key, g_active_effect, g_pub)
#     else:
#         add_subscribers_for_property(target, key, g_active_effect, PubEnum.PROPERTY)
#
#
# def trigger(target, key):
#     trigger_subscribers_for_property(target, key)
#
#
# class ActivateEffect:
#     def __init__(self, effect, pub=PubEnum.PROPERTY):
#         self.effect = effect
#         self.pub = pub
#
#     def __enter__(self):
#         global g_active_effect
#         global g_pub
#         g_active_effect = self.effect
#         g_pub = self.pub
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         global g_active_effect
#         global g_pub
#         g_active_effect = None
#         g_pub = None
#
#
# class Dep:
#     def __init__(self):
#         self.subs: List[WatcherBase] = []
#
#     def add_sub(self, sub):
#         if sub in self.subs:
#             return
#
#         self.subs.append(sub)
#
#     def reset_subs(self):
#         self.subs.clear()
#
#     def notify(self):
#         for sub in self.subs:
#             sub.update()
#
#
# class DepStoreField:
#     _deps: Dict[int, Dict[str, Dep]] = {}
#
#     def __init__(self):
#         pass
#
#     @classmethod
#     def reset(cls):
#         cls._deps = {}
#
#     def __get__(self, instance, owner):
#         instance_id = id(instance)
#         if instance_id not in self._deps:
#             self._deps[instance_id] = defaultdict(Dep)
#
#         return self._deps[instance_id]
#
#     def __set__(self, instance, new_value):
#         pass
#
#     def __delete__(self, instance):
#         instance_id = id(instance)
#         if instance_id in self._deps:
#             del self._deps[instance_id]
#
#
# class Reactive(metaclass=abc.ABCMeta):
#     _deps = DepStoreField()
#
#     @abc.abstractmethod
#     def add_dep(self, attr, sub):
#         pass
#
#     @abc.abstractmethod
#     def reset_deps(self):
#         pass
#
#
# class ReactiveDict(dict, Reactive):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     def __getitem__(self, attr):
#         track(self, attr)
#         return super().__getitem__(attr)
#
#     def __setitem__(self, attr, value):
#         super().__setitem__(attr, value)
#         trigger(self, attr)
#
#     def __getattr__(self, attr):
#         return self.__getitem__(attr)
#
#     def __setattr__(self, attr, value):
#         self.__setitem__(attr, value)
#
#     def __delete__(self, instance):
#         del self._deps
#
#     def add_dep(self, attr, sub):
#         self._deps[attr].add_sub(sub)
#
#     def reset_deps(self):
#         for k, v in self.items():
#             clear_subscribers_for_property(self, k, PubEnum.PROPERTY)
#             if isinstance(v, Reactive):
#                 v.reset_deps()
#
#
# class ReactiveList(list, Reactive):
#     _SUB_KEY = '__reactive_list_sub_key'
#
#     def append(self, __object) -> None:
#         super().append(__object)
#         trigger(self, self._SUB_KEY)
#
#     def extend(self, __iterable) -> None:
#         super().extend(__iterable)
#         trigger(self, self._SUB_KEY)
#
#     def insert(self, __index: SupportsIndex, __object) -> None:
#         super().insert(__index, __object)
#         trigger(self, self._SUB_KEY)
#
#     def __setitem__(self, key, value):
#         super().__setitem__(key, value)
#         trigger(self, self._SUB_KEY)
#
#     def sort(self, *, key: None = ..., reverse: bool = ...) -> None:
#         super().sort(key=key, reverse=reverse)
#         trigger(self, self._SUB_KEY)
#
#     def reverse(self) -> None:
#         super().reverse()
#         trigger(self, self._SUB_KEY)
#
#     def pop(self, __index: SupportsIndex = ...):
#         ret = super().pop(__index)
#         trigger(self, self._SUB_KEY)
#         return ret
#
#     def remove(self, __value) -> None:
#         super().remove(__value)
#         trigger(self, self._SUB_KEY)
#
#     def __delete__(self, instance):
#         del self._deps
#
#     def add_dep(self, sub):
#         add_subscribers_for_property(self, self._SUB_KEY, sub)
#
#     def reset_deps(self):
#         clear_subscribers_for_property(self, self._SUB_KEY, PubEnum.PROPERTY)
#         for item in self:
#             if isinstance(item, Reactive):
#                 item.reset_deps()
#
#
# def observe(data):
#     if isinstance(data, Reactive):
#         data.reset_deps()
#
#     if isinstance(data, dict):
#         for attr, item in data.items():
#             data[attr] = observe(item)
#         if not isinstance(data, Reactive):
#             data = ReactiveDict(data)
#
#     elif isinstance(data, list):
#         for i, item in enumerate(data):
#             data[i] = observe(item)
#         if not isinstance(data, Reactive):
#             data = ReactiveList(data)
#
#     return data


# class VueRef(Reactive):
#     _SUB_KEY = '__ref_sub_key'
#
#     def __init__(self, value):
#         super().__init__()
#         self._value = value
#
#     @property
#     def value(self):
#         track(self, self._SUB_KEY)
#         return self._value
#
#     @value.setter
#     def value(self, new_value):
#         self._value = new_value
#         trigger(self, self._SUB_KEY)
#
#     def add_dep(self, sub):
#         add_subscribers_for_property(self, self._SUB_KEY, sub)
#
#     def reset_deps(self):
#         clear_subscribers_for_property(self, self._SUB_KEY, PubEnum.PROPERTY)
#         if isinstance(self._value, Reactive):
#             self._value.reset_deps()


# def ref(value):
#     return VueRef(value)
#
#
# def reactive(obj):
#     return observe(obj)


# def computed(func, setter=None):
#     val_ref = ref(None)
#     watcher = WatcherForComputed(val_ref, func)
#     with ActivateEffect(watcher, PubEnum.SETUP):
#         val_ref.value = func()
#     return val_ref


# def watch(source, callback, options=None):
#     def _watch_reactive_obj(data: Reactive, source, callback):
#         if isinstance(data, dict):
#             for attr, item in data.items():
#                 _watch_reactive_obj(item, source, callback)
#
#         elif isinstance(data, list):
#             for i, item in enumerate(data):
#                 _watch_reactive_obj(item, source, callback)
#
#     options = options or {}
#     watcher = WatcherForWatchFunc(source, callback, options)
#     with ActivateEffect(watcher, PubEnum.SETUP):
#         if isinstance(source, VueRef):
#             _ = source.value
#         elif isinstance(source, Reactive):
#             _watch_reactive_obj(source, source, callback)
#         elif callable(source):
#             deep = options.get('deep', True)
#             _ = source()
#
#
# class WatcherForRerender(WatcherBase):
#     def __init__(self, vm, name):
#         self.vm = vm
#         self.name = name
#
#     def update(self):
#         self.vm.render()
#
#
# class WatcherForComputed(WatcherBase):
#     def __init__(self, source, func, options=None):
#         self.source = source
#         self.func = func
#         self.value = self.get_val()
#
#     def get_val(self):
#         return self.func()
#
#     def update(self):
#         old_val = self.value
#         new_val = self.get_val()
#         try:
#             if new_val == self.value:
#                 return
#         except Exception as e:
#             pass
#
#         self.value = new_val
#         self.source.value = new_val


# class WatcherForWatchFunc(WatcherBase):
#     def __init__(self, source, callback, options=None):
#         self.source = source
#         self.callback = callback
#         self.value = self.get_val()
#
#     def get_val(self):
#         if isinstance(self.source, VueRef):
#             return self.source.value
#         else:
#             return self.source
#
#     def update(self):
#         old_val = self.value
#         new_val = self.get_val()
#         try:
#             if new_val == self.value:
#                 return
#         except Exception as e:
#             pass
#
#         self.value = new_val
#         self.callback(new_val, old_val)
#
#
# class WatcherForAttrUpdate(WatcherBase):
#     def __init__(self, ns: "VueCompNamespace", val_expr_or_fn, callback, options=None):
#         self.callback = callback
#         self.val_expr_or_fn = val_expr_or_fn
#         self.ns = ns
#         self.value = self.get_val()
#
#     def get_val(self):
#         if callable(self.val_expr_or_fn):
#             return self.val_expr_or_fn()
#         else:
#             return self.val_expr_or_fn.eval(self.ns)
#
#     def update(self):
#         new_val = self.get_val()
#         old_val = self.value
#         try:
#             if new_val == old_val:
#                 return
#         except Exception as e:
#             pass
#
#         self.value = new_val
#         self.callback(new_val, old_val)

@dataclasses.dataclass
class VForAst:
    iter: str
    target: str
    idx: str = None

    @classmethod
    def parse(cls, exp):
        """
        (i, target) in iter
        :param exp:
        :return:
        """
        if not exp:
            return None

        try:
            i_target, iters = [i.strip() for i in exp.split(' in ')]
            i_target = [i.strip() for i in i_target.strip('()').split(',')]
            if len(i_target) == 1:
                i, target = None, i_target[0]
            else:
                i, target = i_target[0], i_target[1]
        except Exception as err:
            msg = f"parse v-for='{exp}' failed, {err}"
            raise ValueError(msg)

        return cls(iter=iters, target=target.strip(), idx=i)


@dataclasses.dataclass
class VForScopes:
    idxs: Tuple[int]
    vars: dict

    def to_ns(self):
        return self.vars


class NodeType(enum.Enum):
    RAW_HTML = 'raw_html'
    WIDGET = 'widget'


@dataclasses.dataclass
class NodeAst:
    tag: str
    attrs: dict = field(default_factory=dict)
    parent: "NodeAst" = None
    children: List["NodeAst"] = field(default_factory=list)
    plain: bool = False
    v_for: VForAst = None
    v_for_scopes: VForScopes = None
    for_processed: bool = False
    type: NodeType = NodeType.WIDGET

    def add_child(self, child):
        self.children.append(child)


@dataclasses.dataclass
class VForNodeAst(NodeAst):

    @property
    def children_flat(self) -> List["NodeAst"]:
        ret = []

        def _travel(children):
            if not isinstance(children, list):
                ret.append(children)
                return

            for child in children:
                _travel(child)

        _travel(self.children)
        return ret


class VForBLockScope:
    def __init__(self, v_for_ast: VForAst, ns):
        self.ns = ns
        self.v_for_ast = v_for_ast

        self.iter = None
        self.target = None
        self.idx = 0
        self.vars_bak = {}
        self.for_vars = {}

    def __enter__(self):
        iter_exp = self.v_for_ast.iter
        if iter_exp in self.ns:
            self.iter = self.ns[iter_exp]
        else:
            self.iter = eval(iter_exp, {}, self.ns)

        target_var = self.v_for_ast.target
        if target_var in self.ns:
            self.vars_bak[target_var] = self.ns[target_var]

        idx_var = self.v_for_ast.idx
        if idx_var in self.ns:
            self.vars_bak[idx_var] = self.ns[idx_var]

        self.for_vars[iter_exp] = self.iter

        return self

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if self.idx >= len(self.iter):
            self.idx = 0
            raise StopIteration()

        # set target
        target_exp = self.v_for_ast.target
        target = self.iter[self.idx]
        self.for_vars[target_exp] = target
        self.ns[target_exp] = target

        if self.v_for_ast.idx is not None:
            # set idx
            idx_exp = self.v_for_ast.idx
            self.for_vars[idx_exp] = self.idx
            self.ns[idx_exp] = self.idx

        self.idx += 1

        return target

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ns.update(self.vars_bak)
        self.vars_bak = {}
        self.for_vars = {}


VForIterFn = Callable[[Tuple[int], dict, VForAst], Any]


def v_for_stack_to_iter(stack: List[VForAst], fn: VForIterFn, ns: dict,
                        for_block_stack_idxs: Tuple[int] = (),
                        for_block_stack_vars: dict = None) -> List[Any]:
    """
    s1 = [1,2]
    s2 = [3,4,5]
    s3 = [6,7]
    for_stack = [s1, s2, s3]
    --
    [ [ [ fn((0, 0, 0), (1, 3, 6)),
          fn((0, 0, 1), (1, 3, 7)) ],
        [ fn((0, 1, 0), (1, 4, 6)),
          fn((0, 1, 1), (1, 4, 7)) ],
        [ fn((0, 2, 0), (1, 5, 6)),
          fn((0, 2, 1), (1, 5, 7)) ]],
      [ [ fn((1, 0, 0), (2, 3, 6)),
          fn((1, 0, 1), (2, 3, 7)) ],
        [ fn((1, 1, 0), (2, 4, 6)),
          fn((1, 1, 1), (2, 4, 7)) ],
        [ fn((1, 2, 0), (2, 5, 6)),
          fn((1, 2, 1), (2, 5, 7)) ]]]

    :param stack:
    :param fn:
    :param ns:
    :param for_block_stack_idxs:
    :param for_block_stack_vars:
    :return:
    """
    if not stack:
        return []

    for_block_stack_vars = for_block_stack_vars or {}
    v_for_ast = stack[0]
    if len(stack) == 1:
        ret = []
        with VForBLockScope(v_for_ast, ns) as for_block_scope:
            for i, val in enumerate(for_block_scope):
                _idxs = (*for_block_stack_idxs, i)
                _vars = {**for_block_stack_vars, **for_block_scope.for_vars}
                ret.append(fn(_idxs, _vars, v_for_ast))
        return ret

    ret = []
    with VForBLockScope(v_for_ast, ns) as for_block_scope:
        for i, val in enumerate(for_block_scope):
            _idxs = (*for_block_stack_idxs, i)
            _vars = {**for_block_stack_vars, **for_block_scope.for_vars}
            ret.append(v_for_stack_to_iter(stack[1:], fn, for_block_scope.ns, _idxs, _vars))
    return ret


# class VForStatement:
#     def __init__(self, target, iters, index=None):
#         self.i = index
#         self.target = target
#         self.iter = iters
#
#     @classmethod
#     def parse(cls, s):
#         """
#         (i, target) in iter
#         :param s:
#         :return:
#         """
#         i_target, iters = [i.strip() for i in s.split(' in ')]
#         i_target = [i.strip() for i in i_target.strip('()').split(',')]
#         if len(i_target) == 1:
#             i, target = None, i_target[0]
#         else:
#             i, target = i_target[0], i_target[1]
#
#         return cls(target.strip(), iters, i)
#
#
# class ForScope:
#     def __init__(self, i_val, for_stmt: VForStatement, vm: 'VueComponent'):
#         self.for_stmt = for_stmt
#         self.i = i_val
#         self.iter = VueCompNamespace.get_by_attr_chain(vm._data, for_stmt.iter)
#         self.target = self.iter[self.i]
#
#     def to_ns(self):
#         return {
#             self.for_stmt.i: self.i,
#             self.for_stmt.target: self.target,
#             self.for_stmt.iter: self.iter,
#         }


class VueCompExprAst:
    def __init__(self, exp_ast, _vars=None, exp_str=''):
        self.vars = _vars if _vars else []
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
    V_ELSE_IF = 'v-else-if'
    V_ELSE = 'v-else'
    V_FOR = 'v-for'
    V_SHOW = 'v-show'
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
        self.v_else_if: VueCompExprAst = None
        self.v_else = False
        self.v_show: VueCompExprAst = None
        # todo rename to attrs
        self.kwargs = {}
        self.v_binds: Dict[str, VueCompExprAst] = {}
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
    def is_v_else_if(cls, attr):
        return attr == cls.V_ELSE_IF

    @classmethod
    def is_v_else(cls, attr):
        return attr == cls.V_ELSE

    @classmethod
    def is_v_show(cls, attr):
        return attr == cls.V_SHOW

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

            elif cls.is_v_else_if(attr):
                comp.v_else_if = vue_comp_expr_parse(value)

            elif cls.is_v_else(attr):
                comp.v_else = True

            elif cls.is_v_show(attr):
                comp.v_show = vue_comp_expr_parse(value)

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
                        ast.Call(
                            func=func_ast.exp_ast.body,
                            args=[Starred(value=Name(id='__vp_args', ctx=Load()), ctx=Load())],
                            keywords=[keyword(value=Name(id='__vp_kwargs', ctx=Load()))],
                        )
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

    # @staticmethod
    # def handle_value_change_vm_to_view(widget, attr):
    #     def warp(val, old_val):
    #         try:
    #             if val == old_val:
    #                 return
    #         except Exception as e:
    #             pass
    #         setattr(widget, attr, val)
    #     return warp
    @classmethod
    def gen(
            cls,
            node: NodeAst,
            vm: 'VueComponent',
            ns: VueCompNamespace,
            app: App
    ):
        comp_ast = VueCompAst.parse(node.tag, node.attrs)
        # v-if
        if comp_ast.v_if:
            dummy = widgets.VBox()

            def _if_cond():
                return comp_ast.v_if.eval(ns)

            @watch(_if_cond, WatchOptions(immediate=True))
            def _change_v_if_widget(cond, old, on_cleanup):
                dummy.children = (cls._gen(comp_ast, node.children, vm, ns, app),) if cond else ()

            # dummy.children = (cls._gen(comp_ast, children, vm, ns, app),) if _if_cond() else ()
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

            # dummy.children = (w,) if _if_show() else ()
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
            app: App
    ):
        component_cls: Type[VueComponent] = vm.component(comp_ast.tag)
        # # v-if
        # if comp_ast.v_if:
        #     # @computed
        #     def should_render():
        #         return comp_ast.v_if.eval(ns)
        #
        #     @watch(should_render)
        #     def rerender(*args):
        #         vm.render()
        #
        #     if not should_render():
        #         return widgets.HTML("")

        # watcher = WatcherForRerender(vm, f'v_if {comp_ast.v_if}')
        # with ActivateEffect(watcher):
        #     if not comp_ast.v_if.eval(ns):
        #         return widgets.HTML("")

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
            # update_vm_to_view = cls.handle_value_change_vm_to_view(widget, widget_attr)
            # watcher = WatcherForAttrUpdate(ns, exp_ast, update_vm_to_view)
            # with ActivateEffect(watcher):
            #     _value = exp_ast.eval(ns)
            # update_vm_to_view(_value, None)

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

            # setattr(widget, widget_attr, _get_v_bind_value())

            # @watchEffect
            # def update_vm_to_view(on_cleanup, _widget_attr=widget_attr):
            #     _old_val = getattr(widget, _widget_attr, Nil)
            #     _new_val = exp_ast.eval(ns)
            #     if has_changed(_old_val, _new_val):
            #         setattr(widget, _widget_attr, to_raw(_new_val))

        # v-model:define-model=bind
        for _model_key, attr_chain in comp_ast.v_model:
            # :bind, parent to child
            # widget_attr = component_cls.v_model_default  # VueCompTag.v_model(comp_ast.tag)
            widget_attr = _model_key
            if _model_key == defineModel.DEFAULT_KEY and hasattr(component_cls, 'v_model_default'):
                widget_attr = getattr(component_cls, 'v_model_default')

            # update_vm_to_view = cls.handle_value_change_vm_to_view(widget, widget_attr)
            # watcher = WatcherForAttrUpdate(ns, lambda: ns.getattr(attr_chain), update_vm_to_view)
            # with ActivateEffect(watcher):
            #     _value = ns.getattr(attr_chain)
            # update_vm_to_view(_value, None)

            def _get_v_model_value(_attr_chain=attr_chain):
                return to_raw(ns.getattr(_attr_chain))

            @watch(_get_v_model_value, WatchOptions(immediate=True))
            def _v_model_update_vm_to_view(curr, old, on_cleanup, _widget_attr=widget_attr):
                _old_val = to_raw(getattr(widget, _widget_attr, Nil))
                curr = to_raw(curr)
                if has_changed(curr, _old_val):
                    setattr(widget, _widget_attr, curr)

            # setattr(widget, widget_attr, _get_v_model_value())

            # @watchEffect
            # def update_vm_to_view(on_cleanup, _widget_attr=widget_attr, _attr_chain=attr_chain):
            #     _old_val = getattr(widget, _widget_attr, Nil)
            #     _new_val = ns.getattr(_attr_chain)
            #     if has_changed(_old_val, _new_val):
            #         setattr(widget, _widget_attr, to_raw(_new_val))

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
            add_event_listener(
                widget,
                f'update:{widget_attr}',
                listener(vm, obj, attr),
            )

        # v-on
        for ev, func_ast in comp_ast.v_on.items():
            def _event_handle(*args, _func_ast=func_ast, **kwargs):
                return _func_ast.eval(ns, {'__vp_args': args, '__vp_kwargs': kwargs})

            add_event_listener(widget, ev, _event_handle)

        if comp_ast.v_ref:
            _ref = ns.getattr(comp_ast.v_ref)
            # if not isinstance(_ref, VueRef):
            if not isinstance(_ref, RefImpl):
                logger.error(f'v-ref={comp_ast.v_ref} needs to be of type Ref.')
            else:
                _ref.value = component if isinstance(component_cls, SFCFactory) else widget

        return widget


def add_event_listener(widget, event, listener):
    if hasattr(widget, SFC.ADD_EVENT_LISTENER_FN):  # SFC
        getattr(widget, SFC.ADD_EVENT_LISTENER_FN)(event, listener)
    elif event.startswith('update:'):  # anywidget, ipyw
        attr = event.split(':', 1)[1]
        widget.observe(listener, names=attr)
    else:  # ipyw click
        getattr(widget, f"on_{event}")(listener)


class VueHtmlTextRender:
    EXP_PATTERN = r"\{\{\s*(.*?)\s*\}\}"

    @staticmethod
    def replace(vm: "VueComponent", ns: VueCompNamespace, for_idx):
        def warp(match):
            exp = match.group(1)
            exp_ast = vue_comp_expr_parse(exp)
            # TODO html可以设置value，按需更新
            # watcher = WatcherForRerender(vm, f'html {for_idx} {{{{ {exp} }}}}')
            # with ActivateEffect(watcher):
            #     _value = exp_ast.eval(ns)
            _value = exp_ast.eval(ns)
            return str(_value)

        return warp

    @classmethod
    def is_raw_html(cls, template):
        return not re.search(cls.EXP_PATTERN, template)

    @classmethod
    def render(cls, template, vm: 'VueComponent', ns: VueCompNamespace, for_idx=-1):
        result = re.sub(cls.EXP_PATTERN, cls.replace(vm, ns, for_idx), template)
        return result


class VueHtmlCompCodeGen:
    @classmethod
    def gen(cls, node: NodeAst, ns: VueCompNamespace):
        comp_ast = VueCompAst.parse(node.tag, node.attrs)

        # @computed
        def __html_tag_exit_gen_html():
            # v-if or v-show
            if_cond = comp_ast.v_if or comp_ast.v_show
            if if_cond and not if_cond.eval(ns):
                return ''

            # v-html
            if comp_ast.v_html:
                attr_chain = comp_ast.v_html
                return ns.getattr(attr_chain)

            # innerHtml
            inner = []
            # for child in node['body']:
            for child in node.children:
                if callable(child):
                    inner.append(child())
                elif isinstance(child, widgets.HTML):
                    inner.append(child.value)
                else:
                    inner.append(child)
            inner_html = ' '.join(inner)

            attrs = [f"{k}='{v}'" for k, v in comp_ast.kwargs.items()]

            # v-bind:
            for attr, exp_ast in comp_ast.v_binds.items():
                attrs.append(f"{attr}='{to_raw(exp_ast.eval(ns))}'")

            html = f'''
                <{node.tag} {' '.join(attrs)}>
                  {inner_html}
                </{node.tag}>'''

            return html

        return __html_tag_exit_gen_html

    @classmethod
    def gen_from_fn(cls, fn):
        widget = widgets.HTML()

        @watch(fn, WatchOptions(immediate=True))
        def _update_html_widget_value(new_html, old_html, on_cleanup):
            widget.value = new_html

        return widget


@dataclasses.dataclass
class SFCFile:
    file: pathlib.Path
    content: str
    template: str
    script_src: str
    script_py: str

    @property
    def setup_fn(self):
        if self.script_src:
            return ScriptCompiler.compile_script_src(self.file.parent, self.script_src)
        elif self.script_py:
            return ScriptCompiler.compile_script_block(
                self.script_py, str(self.file.absolute()))
        else:
            return lambda *args: {}

    @classmethod
    def load(cls, sfc_file):
        sfc_file = pathlib.Path(sfc_file)
        with open(sfc_file) as f:
            raw_content = f.read()

        content = re.sub(r'<!--(.*?)-->', '\n', raw_content, re.S)
        instance = cls(
            file=sfc_file,
            content=raw_content,
            template=cls.get_block_content('template', content)[0],
            script_src=cls.get_script_src(content),
            script_py=cls.get_script_py(content),
        )
        if instance.script_py and instance.script_src:
            raise ValueError(
                "Syntax error: script lang and script src cannot exist at the same time"
            )

        return instance

    @staticmethod
    def get_block_content(tag, content):
        blocks = re.findall(f'<{tag}>(.*)</{tag}>', content, flags=re.S | re.I)
        return blocks

    @staticmethod
    def get_script_src(content):
        match = re.search(r"<script (.*?)src=(['\"])(?P<src>.*?)\2></script>", content)
        return match.group('src') if match else None

    @staticmethod
    def get_script_py(content):
        match = re.search(
            fr'<script\s+lang=(["\'])py\1\s*>(?P<content>.*)?</script>',
            content,
            flags=re.S | re.I
        )

        if not match:
            logger.debug("can't find <script lang=py>")
            return None

        return match.group('content')


class CompilerError(Exception):
    pass


class CompilerSyntaxError(CompilerError):
    def __init__(self, msg):
        super().__init__(f"Syntax Error: {msg}.")


class DomCompiler(HTMLParser):
    """
    @vue/compiler-dom
    """

    def __init__(self, vm: VueComponent, app: 'App'):
        super().__init__()
        self.vm = vm
        self.app = app
        self.widgets = NodeAst('dummy', children=[])
        self.widgets_by_id = {}
        self.parent_node_stack: List[NodeAst | VForNodeAst] = []
        self.v_for_stack: List[VForAst] = []
        self.v_if_stack: List[str] = []
        self._tag = self.widgets.tag

    def _get_element_by_id(self, el_id):
        return self.widgets_by_id.get(el_id)

    @property
    def is_in_for_stmt(self):
        return bool(self.v_for_stack)

    def _process_directive(self):
        pass

    # def _gen_ast_node(self, tag, attrs, for_scope=None):
    #     if self.vm.component(tag):
    #         # node = self._component_tag_enter(tag, attrs, for_scope)
    #         node = {"tag": tag, 'attrs': attrs, 'body': []}
    #     else:
    #         # node = self._html_tag_enter(tag, attrs)
    #         node = {'tag': tag, 'attrs': attrs, 'body': [], 'type': 'html'}
    #     return node

    def _gen_widget(self, node: NodeAst, for_scope: VForScopes = None):
        local_vars = for_scope and for_scope.to_ns()
        ns = VueCompNamespace(self.vm.to_ns(), self.vm.to_ns(), local_vars)
        if self.vm.component(node.tag):
            widget = VueCompCodeGen.gen(node, self.vm, ns, self.app)
        else:
            widget = VueHtmlCompCodeGen.gen(node, ns)

        return widget

    # def _component_tag_enter(self, tag, attrs, for_scope=None):
    #     return {"tag": tag, 'attrs': attrs, 'body': []}
    #
    # def _component_tag_exit(self, node: NodeAst, for_scope: ForScope | VForScopes =None):
    #     comp_ast = VueCompAst.parse(node.tag, node.attrs)
    #     local = for_scope.to_ns() if for_scope else None
    #     ns = VueCompNamespace(self.vm._data, self.vm.to_ns(), local)
    #     widget = VueCompCodeGen.gen(comp_ast, node.children, self.vm, ns, self.app)
    #     return widget
    #
    # def _html_tag_enter(self, tag, attrs):
    #     ast_node = {'type': 'html', 'tag': tag, 'attrs': attrs, 'body': []}
    #     return ast_node
    #
    # def _html_tag_exit(self, node, for_scope: ForScope = None):
    #     # TODO 重构
    #     comp_ast = VueCompAst.parse(node['tag'], node['attrs'])
    #     local = for_scope.to_ns() if for_scope else None
    #     ns = VueCompNamespace(self.vm._data, self.vm.to_ns(), local)
    #     # v-if
    #     widget = widgets.HTML("")
    #     if comp_ast.v_if:
    #         watcher = WatcherForRerender(self.vm, f'v_if {comp_ast.v_if}')
    #         with ActivateEffect(watcher):
    #             if not comp_ast.v_if.eval(ns):
    #                 return widget
    #
    #     tag = node['tag']
    #     attr = ' '.join([f"{k}='{v}'" for k, v in node['attrs'].items()])
    #     html_temp = f"<{tag} {attr}>{{inner_html}}</{tag}>"
    #
    #     def gen_html(inner_html):
    #         return html_temp.format(inner_html=inner_html)
    #
    #     def handle_value_change_vm_to_view(widget, attr):
    #         def warp(val, old_val):
    #             if val == old_val:
    #                 return
    #             setattr(widget, attr, gen_html(val))
    #         return warp
    #
    #     # v-html
    #     if comp_ast.v_html:
    #         attr_chain = comp_ast.v_html
    #         update_vm_to_view = handle_value_change_vm_to_view(widget, 'value')
    #         watcher = WatcherForAttrUpdate(ns, lambda: ns.getattr(attr_chain), update_vm_to_view)
    #         with ActivateEffect(watcher):
    #             _value = ns.getattr(attr_chain)
    #         update_vm_to_view(_value, None)
    #     else:
    #         body = [
    #             child.value if isinstance(child, widgets.HTML) else child
    #             for child in node['body']
    #         ]
    #         widget.value = gen_html(' '.join(body))
    #
    #     return widget

    # def _html_tag_exit(self, node: NodeAst, for_scope: ForScope | VForScopes = None):
    #     # TODO 重构 移到gen里
    #     # comp_ast = VueCompAst.parse(node['tag'], node['attrs'])
    #     comp_ast = VueCompAst.parse(node.tag, node.attrs)
    #     local = for_scope.to_ns() if for_scope else None
    #     ns = VueCompNamespace(self.vm._data, self.vm.to_ns(), local)
    #
    #     def __html_tag_exit_gen_outerhtml(inner_html):
    #         tag = node.tag
    #         attr = ' '.join([f"{k}='{v}'" for k, v in node.attrs.items()])
    #         html_temp = f"<{tag} {attr}>{{inner_html}}</{tag}>"
    #         return html_temp.format(inner_html=inner_html)
    #
    #     # @computed
    #     def __html_tag_exit_gen_html():
    #         # v-if or v-show
    #         if_cond = comp_ast.v_if or comp_ast.v_show
    #         if if_cond and not if_cond.eval(ns):
    #             return ''
    #
    #         # v-html
    #         if comp_ast.v_html:
    #             attr_chain = comp_ast.v_html
    #             return ns.getattr(attr_chain)
    #
    #         # innerHtml
    #         inner = []
    #         # for child in node['body']:
    #         for child in node.children:
    #             if callable(child):
    #                 inner.append(child())
    #             elif isinstance(child, widgets.HTML):
    #                 inner.append(child.value)
    #             else:
    #                 inner.append(child)
    #
    #         return __html_tag_exit_gen_outerhtml(' '.join(inner))
    #
    #     return __html_tag_exit_gen_html

    # def _for_stmt_enter(self, for_stmt: VForStatement, tag, attrs, is_body):
    #     body = []
    #     _iter = VueCompNamespace.get_by_attr_chain(self.vm._data, for_stmt.iter)
    #     for i, target in enumerate(_iter):
    #         for_scope = (i, target)
    #         body.append(self._gen_ast_node(tag, attrs, for_scope))
    #
    #     if is_body:
    #         ast_node = {
    #             "tag": 'v_for',
    #             'v_for_body': for_stmt,
    #             "body": body,
    #         }
    #     else:
    #         ast_node = {
    #             "tag": 'v_for',
    #             'v_for': for_stmt,
    #             "body": body,
    #         }
    #     return ast_node
    #
    # def _for_stmt_exit(self, v_for_ast_node, is_body=False):
    #     _widgets = []
    #     v_for_stmt = self.v_for_stack[-1]
    #     _iter = VueCompNamespace.get_by_attr_chain(self.vm._data, v_for_stmt.iter)
    #     for i, target in enumerate(_iter):
    #         for_scope = ForScope(i, v_for_stmt, self.vm)
    #         node = v_for_ast_node['body'][i]
    #         widget = self._gen_widget(node, for_scope)
    #         if widget:
    #             _widgets.append(widget)
    #
    #     # todo 加到v-for的解析处
    #     if not is_body:
    #         ns = VueCompNamespace(self.vm._data, self.vm.to_ns())
    #         attr_chain = v_for_stmt.iter
    #
    #         def __track_list_change():
    #             # track list replacements
    #             obj_iter = ns.getattr(attr_chain)
    #             # track changes in the list itself, such as append, pop...
    #             return id(obj_iter), [id(item) for item in obj_iter]
    #
    #         @watch(__track_list_change)
    #         def __track_list_change_rerender(new, old, on_cleanup):
    #             self.vm.render()
    #
    #         # _attrs = attr_chain.split('.', 1)
    #         # if len(_attrs) > 1:
    #         #     base_attr, sub_attr_chain = _attrs
    #         #     obj = ns.getattr(base_attr)
    #         #     watcher = WatcherForRerender(self.vm, f"for_stme {v_for_stmt.iter} replace")
    #         #     with ActivateEffect(watcher):
    #         #         VueCompNamespace.get_by_attr_chain(obj, sub_attr_chain)
    #         #
    #         # # 处理list本身的变化，append、pop等操作
    #         # # watcher = WatcherForRerender(self.vm, f"{v_for_stmt.iter} modified")
    #         # # with ActivateEffect(watcher):
    #         # obj_iter = ns.getattr(v_for_stmt.iter)
    #         # if isinstance(obj_iter, Reactive):
    #         #     obj_iter.add_dep(WatcherForRerender(self.vm, f"{v_for_stmt.iter} modified"))
    #
    #     return _widgets

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
        def _gen_node_ast(tag, attrs, for_processed: bool = False, idxs: Tuple[int] = None,
                          vars: dict = None, v_for: VForAst = None) -> NodeAst:
            idxs = idxs or []
            if self.parent_node_stack:
                _parent = self.parent_node_stack[-1]
                _parent = _parent.children if isinstance(_parent, VForNodeAst) else _parent
            else:
                _parent = self.widgets

            for idx in (idxs[:-1] if for_processed else idxs):
                _parent = _parent[idx]

            _for_scopes = VForScopes(idxs=idxs, vars=vars) if idxs and vars else None
            _node = NodeAst(
                tag=tag, attrs=attrs, parent=_parent, children=[], plain=False, v_for=v_for,
                v_for_scopes=_for_scopes, for_processed=for_processed,
                type=node_type
            )
            return _node

        raw_tag = self._get_raw_tag(case_insensitive_tag)
        tag = self._to_camel_case_tag(raw_tag)
        node_type = NodeType.WIDGET if self.vm.component(tag) else NodeType.RAW_HTML
        self._tag = tag
        attrs = dict(attrs)
        self._transformer_node_attrs(attrs)

        v_for_expr = attrs.pop(VueCompAst.V_FOR, None)
        v_for_ast = VForAst.parse(v_for_expr)
        for_processed = False
        if v_for_ast:
            for_processed = True
            self.v_for_stack.append(v_for_ast)

        if self.v_for_stack:
            nodes = v_for_stack_to_iter(
                self.v_for_stack,
                functools.partial(_gen_node_ast, tag, attrs, for_processed),
                self.vm._data
            )
            node = VForNodeAst(tag, attrs, children=nodes, for_processed=for_processed,
                               type=node_type)
        else:
            node = _gen_node_ast(tag, attrs, for_processed)
        self.parent_node_stack.append(node)

        # v_for_stmt = attrs.pop(VueCompAst.V_FOR, None)
        #
        # if v_for_stmt or self.v_for_stack:
        #     is_header = bool(v_for_stmt)
        #     if is_header:
        #         v_for = VForStatement.parse(v_for_stmt)
        #         self.v_for_stack.append(v_for)
        #     v_for = self.v_for_stack[-1]
        #     node = self._for_stmt_enter(v_for, tag, attrs, not is_header)
        # else:
        #     node = self._gen_ast_node(tag, attrs)
        # self.parent_node_stack.append(node)

    def _transformer_node_attrs(self, attrs: dict) -> None:
        prev_v_if_expr = self.v_if_stack.pop() if self.v_if_stack else ''

        _v_if_expr = attrs.get(VueCompAst.V_IF)
        if _v_if_expr:
            return

        v_else_if_expr = attrs.pop(VueCompAst.V_ELSE_IF, '')
        if v_else_if_expr:
            if not prev_v_if_expr:
                _err_msg = f"v-else-if={v_else_if_expr} error, there is no corresponding v-if"
                raise CompilerSyntaxError(_err_msg)

            v_else_if_expr = f"(not ({prev_v_if_expr})) and ({v_else_if_expr})"
            attrs[VueCompAst.V_IF] = v_else_if_expr
            # self.v_if_stack.append(v_else_if_expr)
            return

        v_else_expr = attrs.pop(VueCompAst.V_ELSE, Nil)
        if v_else_expr is not Nil:
            if not prev_v_if_expr:
                _err_msg = f"v-else error, there is no corresponding v-if"
                raise CompilerSyntaxError(_err_msg)

            # if_expr = self.v_if_stack.pop()
            v_else_expr = f"not ({prev_v_if_expr})"
            attrs[VueCompAst.V_IF] = v_else_expr
            return

    def handle_data(self, data: str) -> None:
        if not self.parent_node_stack:
            return

        if not data.strip():
            return

        tag = self._tag

        def _gen_text(node: NodeAst, should_render: bool):
            if isinstance(node, VForNodeAst):
                for _node in node.children_flat:
                    _gen_text(_node, should_render)
                return

            ns = VueCompNamespace(self.vm.to_ns(), self.vm.to_ns(),
                                  node.v_for_scopes and node.v_for_scopes.to_ns())
            i = -1
            if node.v_for_scopes:
                i = node.v_for_scopes.idxs[-1]

            def __handle_data_gen_html(_ns=ns, _i=i, _should_render=should_render):
                if _should_render:
                    logger.debug("for_stmt_gen_html index=%s <%s> tmpl=`%s`", _i, tag, data)
                    return VueHtmlTextRender.render(data, self.vm, _ns, _i)
                else:
                    return data

            if node.type == NodeType.RAW_HTML:
                node.add_child(__handle_data_gen_html)
            else:
                node.add_child(VueHtmlCompCodeGen.gen_from_fn(__handle_data_gen_html))

        should_render = not VueHtmlTextRender.is_raw_html(data)
        parent = self.parent_node_stack[-1]
        _gen_text(parent, should_render)

        #
        #
        # if not self.is_in_for_stmt:
        #     if parent.type != NodeType.RAW_HTML:
        #         logger.warning(f"<{tag}> not support innerText.")
        #         return
        #
        #     ns = VueCompNamespace(self.vm._data, self.vm.to_ns())
        #
        #     # result = VueCompHtmlTemplateRender.render(data, self.vm, ns, -1)
        #     # parent['body'].append(result)
        #
        #     def __handle_data_gen_html(_should_render=should_render):
        #         return VueCompHtmlTemplateRender.render(data, self.vm, ns, -1) if _should_render else data
        #
        #     parent.add_child(__handle_data_gen_html)
        #     # parent['body'].append(__handle_data_gen_html)
        #
        # # v-for
        # # TODO node的类型判断可以优化
        # elif parent['body'] and parent['body'][0].get('type') == 'html':
        #     v_for_stmt = self.v_for_stack[-1]
        #     _iter = VueCompNamespace.get_by_attr_chain(self.vm._data, v_for_stmt.iter)
        #     for i, _ in enumerate(_iter):
        #         for_scope = ForScope(i, v_for_stmt, self.vm)
        #         ns = VueCompNamespace(self.vm._data, self.vm.to_ns(), for_scope.to_ns())
        #
        #         def __handle_data_for_stmt_gen_html(_ns=ns, _i=i, _should_render=should_render) -> str:
        #             if _should_render:
        #                 logger.debug("for_stmt_gen_html index=%s <%s> tmpl=`%s`", _i, tag, data)
        #                 return VueCompHtmlTemplateRender.render(data, self.vm, _ns, _i)
        #             else:
        #                 return data
        #
        #         parent['body'][i]['body'].append(__handle_data_for_stmt_gen_html)
        # else:
        #     logger.error(f"miss match `{repr(data)}`")

    # def handle_endtag_bak(self, tag):
    #     node = self.parent_node_stack.pop()
    #     if self.is_in_for_stmt:
    #         is_body = 'v_for' not in node
    #         _widgets = self._for_stmt_exit(node, is_body)
    #         if is_body:
    #             for i, widget in enumerate(_widgets):
    #                 self.parent_node_stack[-1]['body'][i]['body'].append(widget)
    #         else:
    #             for i, _widget in enumerate(_widgets):
    #                 if callable(_widget):
    #                     _widgets[i] = VueHtmlCompRender.gen_from_fn(_widget)
    #             self.parent_node_stack[-1]['body'].extend(_widgets)
    #             self.v_for_stack.pop()
    #     else:
    #         widget = self._gen_widget(node)
    #         if not widget:
    #             return
    #
    #         if callable(widget):
    #             widget = VueHtmlCompRender.gen_from_fn(widget)
    #
    #         if self.parent_node_stack:
    #             self.parent_node_stack[-1]['body'].append(widget)
    #         else:
    #             self.widgets.add_child(widget)

    def handle_endtag(self, tag):
        def _gen_element(_node: NodeAst):
            if isinstance(_node, VForNodeAst):
                for _node in _node.children_flat:
                    _gen_element(_node)
                return

            widget = self._gen_widget(_node, _node.v_for_scopes)
            # not v-for
            if not _node.v_for_scopes:
                widget = VueHtmlCompCodeGen.gen_from_fn(widget) if callable(widget) else widget
                _node.parent.add_child(widget)
            # curr v-for end
            elif _node.for_processed:
                widget = VueHtmlCompCodeGen.gen_from_fn(widget) if callable(widget) else widget
                _node.parent.add_child(widget)

                # todo 加到v-for的解析处
                ns = VueCompNamespace(self.vm.to_ns(), self.vm.to_ns())
                attr_chain = _node.v_for.iter

                def __track_list_change():
                    # track list replacements
                    obj_iter = ns.getattr(attr_chain)
                    # track changes in the list itself, such as append, pop...
                    return id(obj_iter), [id(item) for item in obj_iter]

                @watch(__track_list_change)
                def __track_list_change_rerender(new, old, on_cleanup):
                    self.vm.render()
            # v-for in process
            else:
                _node.parent.add_child(widget)

        node = self.parent_node_stack.pop()
        _gen_element(node)
        if node.for_processed:
            self.v_for_stack.pop()

        v_if_expr = node.attrs.get(VueCompAst.V_IF)
        if v_if_expr:
            self.v_if_stack.append(v_if_expr)

    def compile(self, html):
        self.html_lines = [line for line in html.splitlines()]
        self.feed(html)
        if len(self.widgets.children) == 1:
            return self.widgets.children[0]
        return widgets.VBox(self.widgets.children)


class ScriptCompiler:
    @staticmethod
    def compile_script_block_bak(code_str, source_file_path):
        indent_code_str = '\n'.join([f"  {line}" for line in code_str.split('\n')])
        code = '\n'.join([
            "def setup(props, ctx, app):",
            indent_code_str,
            "\n",
            "  return locals()",
        ])

        module = types.ModuleType('tmp_module')
        module.__dict__['__file__'] = source_file_path
        exec(code, module.__dict__)
        return module.setup

    @staticmethod
    def compile_script_block(code_str, source_file_path):
        module = ast.parse(code_str)
        func_name = 'setup'
        func_ast = ast.FunctionDef(
            name=func_name,
            args=ast.arguments(
                posonlyargs=[],
                args=[
                    ast.arg(arg='props', annotation=None),
                    ast.arg(arg='ctx', annotation=None),
                    ast.arg(arg='app', annotation=None)
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

        pymodule = types.ModuleType('tmp_module')
        pymodule.__dict__['__file__'] = source_file_path
        exec(code, pymodule.__dict__)
        return pymodule.setup

    @staticmethod
    def compile_script_src(dir_path, src):
        _script_path = dir_path.joinpath(src)
        if not _script_path.exists():
            raise ValueError(f"sfc script {_script_path} not exists.")

        _spec = importlib.util.spec_from_file_location('sfc', str(_script_path))
        _module = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_module)
        return getattr(_module, 'setup')

    # @classmethod
    # def compile(cls, sfc_file):
    #     sfc_file = pathlib.Path(sfc_file)
    #     script_src = get_script_src_from_sfc(sfc_file)
    #     if script_src:
    #         return cls.compile_script_src(sfc_file.parent, script_src)
    #
    #     script_block = get_script_py_block_content_from_sfc(sfc_file)
    #     if not script_block:
    #         return lambda *args: {}
    #
    #     return cls.compile_script_block(script_block, str(sfc_file.absolute()))


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
class Record:
    def to_ns(self):
        return self.__dict__


@dataclasses.dataclass
class AppConfig:
    """应用的配置设定"""
    # error_handler: ErrorHandler
    # warn_handler: WarningHandler
    # option_merge_strategies: dict[str, OptionMergeFunction] = {}
    globalProperties: Record = field(default_factory=Record)
    compilerOptions: CompilerOptions = CompilerOptions()
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


class App:
    version = '0.0.1'
    components = {}

    def __init__(self, root_component: RootComponent, debug=False):
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
            self.root_component: SFC = root_component.gen(props, context, self)
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
        logger.info('App render start.')
        if not isinstance(self.root_component, SFC):
            raise ValueError(f"render failed, root_component type {type(self.root_component)}.")

        # self.dom = self.options.render({}, self._props, self._data)
        self.dom = self.root_component.render()
        # with self.options.el:
        with self._container:
            clear_output(True)
            display(self.dom)
        logger.info('App render end.')

    def component(self, name: str, comp: 'VueComponent' = None) -> App:
        """
        query component(name) -> Component | None
        register component(name, comp) -> self

        :param name:
        :param comp:
        :return: self
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

    def use(self, plugin: Type["VuePlugin"], options: dict = None) -> "App":
        """
        install plugin.

        :param plugin: 插件本身
        :param options: 要传递给插件的选项
        :return: self
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
        comp = self.to_ns().get(name)
        try:
            if comp and (isinstance(comp, SFCFactory) or issubclass(comp, VueComponent)):
                return comp
        except Exception as e:
            logger.warn(f"find component({name}) in Component `{self.name()}` failed, {e}.")
            pass

        comp = self.app.component(name)
        # if comp is None:
        #     logger.warn(f"component({name}) not found in Component `{self.name()}`.")

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
    def __init__(self, prop_name: str, default=None):
        self.name = prop_name
        self._value = ref(default, debug_msg=f"prop:{prop_name}")

    @property
    def value(self):
        return self._value.value

    @value.setter
    def value(self, val):
        self._value.value = val


class DefineProps:
    def __init__(self, props: dict | list, init_vals: dict = None):
        self.prop_names = props
        self.props: List[DefineProp] = [
            DefineProp(name, init_vals.get(name)) for name in self.prop_names
        ]
        for prop in self.props:
            setattr(self, prop.name, prop)


def get_caller_args(frame):
    if not frame:
        return []

    caller_name = frame.f_code.co_name
    caller_func = frame.f_globals.get(caller_name)
    if not caller_func:
        logger.warn(f"can't get caller_func<{caller_name}>")
        return []

    argspec = inspect.getfullargspec(caller_func)
    if not argspec.args:
        logger.warn(f"get caller_func<{caller_name}> args is None")
        return []

    return [frame.f_locals.get(arg_name) for arg_name in argspec.args]


def defineProps(props: dict | list):
    """
    props = defineProps('p1')
    props.p1.value
    """
    frame = inspect.currentframe().f_back
    caller_args = get_caller_args(frame)
    init_props = caller_args[0] if caller_args else {}
    init_attrs = caller_args[1].get('attrs', {}) if len(caller_args) >= 2 else {}
    init_vals = {**init_props, **init_attrs}

    return DefineProps(props, init_vals)


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

    def __call__(self, event, *args, **kwargs):
        """$emit event.

        :param event:
        :param args: payload
        :param kwargs: payload
        :return:
        """
        handlers = self.events_to_cb_dispatcher.get(event)
        if not handlers:
            raise Exception(f"Event {event} not supported.")
        handlers(*args, **kwargs)


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
        logger.debug("defineModel:%s set value %s to %s", self.model_key, self.prop.value, val)
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
    def define_props(self) -> (str, DefineProps):
        ret = self._get_define_x(DefineProps, limit=1)
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

    # def clear_property_subs(self):
    #     for item in self._data.values():
    #         if isinstance(item, Reactive):
    #             item.reset_deps()
    def __repr__(self):
        return f"{self.__class__.__name__}<{pathlib.Path(self.file).name}> at {id(self)}"

    def render(self, ctx: SetupContext = None, props: dict = None, setup_returned: dict = None) -> VNode:
        # self.clear_property_subs()
        logger.info(f"🔥 Rerender {self}")
        self.scope.clear()

        with self.scope:
            if self._render:
                dom = self._render(self._context, self._props, self.setup_returned)
            else:
                dom = DomCompiler(self, self.app).compile(self.template)

        self.root.children = [dom]

        return self.root


@dataclasses.dataclass
class SFCFactory:
    # (props: dict, context: SetupContext, app: App) -> dict | Callable[[], h]:
    setup: Callable[[dict, SetupContext | dict, 'App'], dict | Callable] = None
    template: str = ''
    # (self, ctx, props, setup_returned) -> VNode:
    render: Callable[[SetupContext | dict, dict, dict], VNode] = None
    _file: str = ''

    def gen(self, props: dict, context: SetupContext | dict, app: App) -> "SFC":
        setup_ret = self.setup(props, context, app) if self.setup else {}
        return SFC(context, props, setup_ret, self.template, app, self.render, self._file)


VueOptions = SFCFactory


def import_sfc(sfc_file):
    sfc_file = SFCFile.load(sfc_file)

    return SFCFactory(**{
        'setup': sfc_file.setup_fn,
        'template': sfc_file.template,
        '_file': sfc_file.file,
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
