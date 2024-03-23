#!coding: utf-8
import abc
import ast
import enum
import importlib.util
import pathlib
import re
import types
from _ast import Attribute
from collections import defaultdict
from html.parser import HTMLParser
from typing import Any
from typing import Dict
from typing import List
from typing import SupportsIndex
from typing import Type

import ipywidgets as widgets
from IPython.display import clear_output
from IPython.display import display

from vuepy import log as logging

LOG = logging.getLogger()


def get_block_content_from_sfc(sfc_file, block):
    with open(sfc_file) as f:
        blocks = re.findall(f'<{block}>(.*)</{block}>', f.read(), flags=re.S)
    return blocks


def get_template_from_vue(sfc_file):
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
    def __init__(self, i_val, for_stmt: VForStatement, vm: 'Vue'):
        self.for_stmt = for_stmt
        self.i = i_val
        self.iter = VueCompNamespace.get_by_attr_chain(vm, for_stmt.iter)
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
    V_JS_LINK = 'v-js-link'
    V_MODEL = 'v-model'
    V_HTML = 'v-html'
    EVENT_PREFIX = '@'
    SINGLE_BOUND_PREFIX = ':'
    LAYOUT_ATTRS = {'width', 'height', 'padding', 'border'}

    # todo 和h函数的参数保持一致
    def __init__(self, tag):
        self.tag = tag
        self.v_if: VueCompExprAst = None
        # todo rename to attrs
        self.kwargs = {}
        self.v_binds: Dict[str, VueCompExprAst] = {}
        # todo support only one v-model
        self.v_model_vm = None
        self.v_html = None
        self.v_on: Dict[str, VueCompExprAst] = {}
        self.layout = {}
        self.v_slot = None

    @classmethod
    def is_v_if(cls, attr):
        return attr == cls.V_IF

    @classmethod
    def is_v_slot(cls, attr):
        return attr.startswith(cls.V_SLOT)

    @classmethod
    def is_v_model(cls, attr):
        return attr == cls.V_MODEL

    @classmethod
    def is_v_html(cls, attr):
        return attr == cls.V_HTML

    @classmethod
    def is_event(cls, attr):
        return attr.startswith(cls.EVENT_PREFIX)

    @classmethod
    def is_single_bound(cls, attr):
        return attr.startswith(cls.SINGLE_BOUND_PREFIX)

    @classmethod
    def is_layout(cls, attr):
        return attr in cls.LAYOUT_ATTRS

    @classmethod
    def parse(cls, tag, attr_dict):
        comp = cls(tag)
        for attr, value in attr_dict.items():
            if cls.is_v_if(attr):
                comp.v_if = vue_comp_expr_parse(value)

            elif cls.is_single_bound(attr):
                attr = attr.lstrip(cls.SINGLE_BOUND_PREFIX)
                comp.v_binds[attr] = vue_comp_expr_parse(value)

            elif cls.is_v_model(attr):
                comp.v_model_vm = value

            elif cls.is_v_html(attr):
                comp.v_html = value

            elif cls.is_event(attr):
                event = attr.lstrip(cls.EVENT_PREFIX)
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

            elif cls.is_v_slot(attr):
                comp.v_slot = attr.split(':', 1)[1]

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
    def gen(cls, comp_ast: VueCompAst, children, vm: 'Vue', ns: VueCompNamespace):
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
        component_cls = vm.find_component(comp_ast.tag)
        if comp_ast.v_model_vm:
            props[component_cls.v_model_default] = ns.getattr(comp_ast.v_model_vm)

        widget = component_cls().render(ctx, props, {})

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

        # v-model:widget=vm
        if comp_ast.v_model_vm:
            attr_chain = comp_ast.v_model_vm
            # vm to view
            widget_attr = component_cls.v_model_default  # VueCompTag.v_model(comp_ast.tag)
            # = :bind
            update_vm_to_view = cls.handle_value_change_vm_to_view(widget, widget_attr)
            watcher = WatcherForAttrUpdate(ns, lambda: ns.getattr(attr_chain), update_vm_to_view)
            with ActivateEffect(watcher):
                _value = ns.getattr(attr_chain)
            update_vm_to_view(_value, None)

            # = v-on
            # view to vm
            def handle_value_change_view_to_vm(obj, attr):
                def warp(change):
                    return setattr(obj, attr, change['new'])

                return warp

            obj, attr = ns.get_obj_and_attr(attr_chain)
            update_view_to_vm = handle_value_change_view_to_vm(obj, attr)
            widget.observe(update_view_to_vm, names=f'{widget_attr}')

        # v-on
        for ev, func_ast in comp_ast.v_on.items():
            getattr(widget, f"on_{ev}")(lambda payload: func_ast.eval(ns, {'__owner': payload}))

        return widget


class VueCompHtmlTemplateRender:
    @staticmethod
    def replace(vm: "Vue", ns: VueCompNamespace, for_idx):
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
    def render(cls, template, vm: 'Vue', ns: VueCompNamespace, for_idx=-1):
        exp_pattern = r"\{\{\s*(.*?)\s*\}\}"
        result = re.sub(exp_pattern, cls.replace(vm, ns, for_idx), template)
        return result


class VueTemplate(HTMLParser):
    """
    @vue/compiler-dom

    数据绑定:
    https://docs.python.org/zh-cn/3.10/library/ast.html#function-and-class-definitions
    https://juejin.cn/post/7242700247440293925
    https://www.chuchur.com/article/vue-mvvm-complie
    https://github.com/leilux/SICP-exercises/blob/master/book/p216-constraint-propagate(python%20version).py
    """

    def __init__(self, vm: 'Vue'):
        super().__init__()
        self.vm = vm
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
        if self.vm.find_component(tag):
            node = self._component_tag_enter(tag, attrs, for_scope)
        else:
            node = self._html_tag_enter(tag, attrs)
        return node

    def _gen_widget(self, node, for_scope=None):
        tag = node['tag']
        if self.vm.find_component(tag):
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
        widget = VueCompCodeGen.gen(comp_ast, node['body'], self.vm, ns)
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

    def handle_starttag(self, tag, attrs):
        tag = ''.join(tag.split('-'))
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
        self.feed(html)
        if len(self.widgets) == 1:
            return self.widgets[0]
        return widgets.VBox(self.widgets)


class VueOptions:
    def __init__(self, options):
        self.el = options.get('el')
        self.data = options.get('data')
        self.setup = options.get('setup')
        self.methods = options.get('methods', {})
        self.template = options.get('template', '')
        try:
            template_path = pathlib.Path(self.template)
            if template_path.exists():
                self.template = get_template_from_vue(template_path)
        except Exception:
            pass

        self.before_create = options.get('before_create')
        self.created = options.get('created')
        self.before_mount = options.get('before_mount')
        self.mounted = options.get('mounted')
        self.before_update = options.get('before_update ')
        self.updated = options.get('updated ')
        self.render = options.get('render')


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


class Vue:
    components = {}

    def __init__(self, options, debug=False):
        options = VueOptions(options)
        # self._data = observe(options.data)
        self._data = options.setup(None, None, self)
        self.debug = debug

        self._components = {}

        self.document: Document = Document()
        self.dom = None
        self.options = options
        self._call_if_callable(self.options.before_create)
        self._call_if_callable(self.options.created)

        # self.methods = self.options.methods(self)
        self._proxy_methods()

    def to_ns(self):
        methods = {
            # m: getattr(self.methods, m)
            # for m in dir(self.methods) if not m.startswith('_')
        }
        return {
            **methods,
            **self._data,
        }

    def _call_if_callable(self, func):
        if callable(func):
            func(self)

    def __getattr__(self, key):
        if key == '_data':
            return super().__getattribute__(key)

        if key in self._data:
            return self._data[key]

        return super().__getattribute__(key)

    def __setattr__(self, key, value):
        if key == '_data':
            return super().__setattr__(key, value)

        if key in self._data:
            self._data[key] = value
            return
        return super().__setattr__(key, value)

    def _proxy_methods(self):
        pass

    def mount(self, el):
        self.options.el = el
        self._call_if_callable(self.options.before_mount)
        self.render()
        self._call_if_callable(self.options.mounted)
        self.document.body.appendChild(self.options.el)
        return self.document

    def _compile_template(self, template):
        vue_template = VueTemplate(self)
        return vue_template.compile(template)

    def clear_property_subs(self):
        for item in self._data.values():
            if isinstance(item, Reactive):
                item.reset_deps()

    def render(self):
        self.clear_property_subs()
        with self.options.el:
            if callable(self.options.template):
                self.dom = self.options.template(self)
            else:
                self.dom = self._compile_template(self.options.template)
            clear_output(True)
            display(self.dom)

    def find_component(self, name) -> 'VueComponent':
        return self._components.get(name, self.components.get(name, None))

    def component(self, name: str, comp: 'VueComponent'):
        self._components[name] = comp
        return self

    def use(self, plugin: Type["VuePlugin"], options: dict = None):
        plugin.install(self, options)
        return self


class VNode:
    def __init__(self, type_, props, children=None, key=''):
        self.type = type_
        self.props = props
        self.children = children
        self.key = key


class VueComponent(metaclass=abc.ABCMeta):
    props = {}
    template = ''
    _name = ''

    v_model_default = 'value'

    @classmethod
    def name(cls):
        return (cls._name or cls.__name__).lower()

    def setup(self, props: dict = None, ctx=None, vm: Vue = None):
        """

        :param props:
        :param ctx: attrs, slots, emit
        :param vm:
        :return:
        """
        pass

    def render(self, ctx, props, setup_returned) -> VNode:
        """
        h(tag, props|attrs, children)

        :param ctx: attrs, slots, emit
        :param setup_returned:
        :param props:
        :return:
        """
        if not self.template:
            return None
        # return vue_compiler_dom(self.template)

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
    def install(cls, vm: Vue, options: dict):
        pass


def import_sfc(sfc_file):
    sfc_file = pathlib.Path(sfc_file)
    script_src = get_script_src_from_sfc(sfc_file)
    script_path = sfc_file.parent.joinpath(script_src)

    spec = importlib.util.spec_from_file_location('sfc', str(script_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {
        'setup': getattr(module, 'setup'),
        'template': sfc_file,
    }


def create_app(root_component: dict, **root_props) -> Vue:
    debug = root_props.get('debug', False)
    return Vue(root_component, debug)

