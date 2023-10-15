#!coding: utf-8
import ast
import functools
import re
from collections import defaultdict
from html.parser import HTMLParser
from typing import SupportsIndex

import ipywidgets as widgets
import markdown
from IPython.display import clear_output
from IPython.display import display


class DepStoreField:
    def __init__(self):
        self._deps = {}

    def __get__(self, instance, owner):
        _id = id(instance)
        if _id not in self._deps:
            self._deps[_id] = defaultdict(Dep)

        return self._deps[_id]

    def __set__(self, instance, new_value):
        pass

    def __delete__(self, instance):
        _id = id(instance)
        if _id in self._deps:
            del self._deps[_id]


class Reactive:
    _deps = DepStoreField()

    def add_dep(self, attr, sub):
        pass

    def reset_deps(self):
        pass


class ReactiveDict(dict, Reactive):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, attr):
        return super().__getitem__(attr)

    def __setitem__(self, attr, value):
        super().__setitem__(attr, value)

        self._deps[attr].notify()

    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __setattr__(self, attr, value):
        self.__setitem__(attr, value)

    def __delete__(self, instance):
        del self._deps

    def add_dep(self, attr, sub):
        self._deps[attr].add_sub(sub)

    def reset_deps(self):
        for attr, dep in self._deps.items():
            dep.reset_subs()


class ReactiveList(list, Reactive):
    def append(self, __object) -> None:
        super().append(__object)
        self._deps[0].notify()

    def extend(self, __iterable) -> None:
        super().extend(__iterable)
        self._deps[0].notify()

    def insert(self, __index: SupportsIndex, __object) -> None:
        super().insert(__index, __object)
        self._deps[0].notify()

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._deps[0].notify()

    def sort(self, *, key: None = ..., reverse: bool = ...) -> None:
        super().sort(key=key, reverse=reverse)
        self._deps[0].notify()

    def reverse(self) -> None:
        super().reverse()
        self._deps[0].notify()

    def pop(self, __index: SupportsIndex = ...):
        ret = super().pop(__index)
        self._deps[0].notify()
        return ret

    def remove(self, __value) -> None:
        super().remove(__value)
        self._deps[0].notify()

    def __delete__(self, instance):
        del self._deps

    def add_dep(self, sub):
        self._deps[0].add_sub(sub)

    def reset_deps(self):
        self._deps[0].reset_subs()


class ListWatcher:
    def __init__(self, vm, name):
        self.vm = vm
        self.name = name

    def update(self):
        self.vm.render()


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


class Dep:
    target = None

    def __init__(self):
        self.subs = []

    def add_sub(self, sub):
        if sub in self.subs:
            return

        self.subs.append(sub)

    def reset_subs(self):
        self.subs.clear()

    def notify(self):
        sub_count = len(self.subs)
        for i in range(sub_count):
            self.subs[i].update()


def get_attr_by_dot_chain(data, dot_chain):
    attrs = dot_chain.split('.')
    _data = data
    for attr in attrs:
        _data = getattr(_data, attr)
    return _data


def set_attr_by_dot_chain(data, dot_chain, val):
    attrs = dot_chain.rsplit('.', 1)
    if len(attrs) == 1:
        attr_set = attrs[0]
        _data = data
    else:
        _attr_get, attr_set = attrs
        _data = get_attr_by_dot_chain(data, _attr_get)

    setattr(_data, attr_set, val)


class Watcher:
    def __init__(self, scopes, expr_or_fn, callback, options=None):
        self.vm = scopes
        self.cb = callback
        self.exp = expr_or_fn
        self.options = options
        self.base_data, self.attr = get_base_from_scopes(scopes, expr_or_fn)
        self.value = self.get()
        self.base_data.add_dep(self.attr, self)

    def get(self):
        value = get_attr(self.base_data, self.attr)
        return value

    def update(self):
        self.run()

    def run(self):
        value = self.get()
        old_val = self.value
        if value != old_val:
            self.value = value
            self.cb(self.vm, value, old_val)


class _MarkdownViewer(widgets.HTML):
    with open('codehilite') as f:
        css_style = ''.join(f.read())

    def __init__(self, value):
        extra = [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.tables',
            # 'markdown.extensions.nl2br',
        ]
        html = markdown.markdown(value, extensions=extra)
        super().__init__(f"<style>{self.css_style}</style>" + html)


class Tag:
    AppLayout = "AppLayout".lower()
    Box = "Box".lower()
    Button = 'Button'.lower()
    Checkbox = 'Checkbox'.lower()
    ColorsInput = 'ColorsInput'.lower()
    Combobox = 'Combobox'.lower()
    Controller = 'Controller'.lower()
    Dropdown = "Dropdown".lower()
    FileUpload = 'FileUpload'.lower()
    FloatsInput = 'FloatsInput'.lower()
    FloatSlider = 'FloatSlider'.lower()
    HBox = 'HBox'.lower()
    HtmlMath = 'HtmlMath'.lower()
    Image = 'Image'.lower()
    InputNumber = 'InputNumber'.lower()
    IntsInput = 'IntsInput'.lower()
    Label = 'Label'.lower()
    MarkdownViewer = 'MarkdownViewer'.lower()
    Password = 'Password'.lower()
    Play = 'Play'.lower()
    Progress = 'Progress'.lower()
    RadioButtons = 'RadioButtons'.lower()
    Select = 'Select'.lower()
    Slider = 'Slider'.lower()
    Stack = 'Stack'.lower()
    TagsInput = 'TagsInput'.lower()
    Text = 'Text'.lower()
    Textarea = 'Textarea'.lower()
    ToggleButton = 'ToggleButton'.lower()
    ToggleButtons = 'ToggleButtons'.lower()
    Valid = 'Valid'.lower()
    Template = 'template'

    _container_tags = (
        AppLayout,
        Box,
        HBox,
        Stack,
        Template,
    )
    _leaf_tags = (
        FloatSlider,
        Checkbox,
        ColorsInput,
        Combobox,
        Controller,
        Dropdown,
        FileUpload,
        FloatsInput,
        FloatSlider,
        Dropdown,
        Textarea,
        Button,
        HtmlMath,
        Image,
        InputNumber,
        IntsInput,
        Label,
        MarkdownViewer,
        Password,
        Play,
        Progress,
        RadioButtons,
        Text,
        Select,
        Slider,
        TagsInput,
        Text,
        Textarea,
        ToggleButton,
        ToggleButtons,
        Valid,
    )

    _tag_to_widget = {
        AppLayout: widgets.AppLayout,
        Box: widgets.VBox,
        Button: widgets.Button,
        Checkbox: widgets.Checkbox,
        ColorsInput: widgets.ColorsInput,
        Combobox: widgets.Combobox,
        Controller: widgets.Controller,
        Dropdown: widgets.Dropdown,
        FileUpload: widgets.FileUpload,
        FloatsInput: widgets.FloatsInput,
        FloatSlider: widgets.FloatSlider,
        HBox: widgets.HBox,
        HtmlMath: widgets.HTMLMath,
        Image: widgets.Image,
        InputNumber: widgets.IntText,  # TODO IntText, FloatText
        IntsInput: widgets.IntsInput,
        Label: widgets.Label,
        MarkdownViewer: _MarkdownViewer,
        Password: widgets.Password,
        Play: widgets.Play,
        Progress: widgets.FloatProgress,
        RadioButtons: widgets.RadioButtons,
        Select: widgets.Select,
        Slider: widgets.FloatSlider,  # TODO xxxSlider
        Stack: widgets.Stack,
        TagsInput: widgets.TagsInput,
        Template: widgets.VBox,
        Text: widgets.Text,
        Textarea: widgets.Textarea,
        ToggleButton: widgets.ToggleButton,
        ToggleButtons: widgets.ToggleButtons,
        Valid: widgets.Valid,
    }

    _tag_to_v_model = {
        Button: 'description',
        Stack: 'selected_index',
    }

    @classmethod
    def is_container(cls, t):
        return t in [i.lower() for i in cls._container_tags]

    @classmethod
    def is_leaf(cls, t):
        return t in [i.lower() for i in cls._leaf_tags]

    @classmethod
    def get_widget(cls, t):
        return getattr(widgets, getattr(cls, t))

    @classmethod
    def impl(cls, tag):
        return cls._tag_to_widget[tag]

    @classmethod
    def v_model(cls, tag):
        return cls._tag_to_v_model.get(tag, 'value')


class VForStatement:
    def __init__(self, target, iters, index=None):
        self.i = index
        self.target = target
        self.iter = iters

    @classmethod
    def parse(cls, s):
        i_target, iters = [i.strip() for i in s.split('in')]
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
        self.iter = get_attr(vm, for_stmt.iter)
        self.target = self.iter[self.i]


class Directive:
    v_if = 'v-if'
    v_for = 'v-for'
    v_slot = 'v-slot:'
    v_js_link = 'v-js-link'
    v_model = 'v-model'
    event_prefix = '@'
    single_bound_prefix = ':'
    layout_attrs = {'width', 'height'}

    @classmethod
    def is_v_if(cls, attr, value):
        return attr == cls.v_if

    @classmethod
    def is_v_for(cls, attr, value):
        if attr == cls.v_for:
            pass

    @classmethod
    def is_v_slot(cls, attr, value):
        if not attr.startswith(cls.v_slot):
            return False, None
        return True, attr.split(':')[1]

    @classmethod
    def is_v_js_link(cls, attr, value):
        if attr == cls.v_js_link:
            return True, None
        return False, None

    @classmethod
    def is_v_model(cls, attr, value):
        if attr == cls.v_model:
            return True, value
        return False, None

    @classmethod
    def is_event(cls, attr: str, func):
        if not attr.startswith(cls.event_prefix):
            return False, attr, None, None
        event = attr.lstrip(cls.event_prefix)
        match = re.match('(.*)\((.*)\)', func)
        if not match:
            return True, event, func, None

        func = match[1]
        args = [i.strip() for i in match[2].split(',')]
        return True, event, func, args

    @classmethod
    def is_single_bound(cls, attr: str, value):
        if attr.startswith(cls.single_bound_prefix):
            return True, attr.lstrip(cls.single_bound_prefix)
        return False, None

    @classmethod
    def is_layout(cls, attr: str, value):
        return attr in cls.layout_attrs


class VueTemplate(HTMLParser):
    """
    数据绑定:
    https://docs.python.org/zh-cn/3.10/library/ast.html#function-and-class-definitions
    https://juejin.cn/post/7242700247440293925
    https://www.chuchur.com/article/vue-mvvm-complie
    https://github.com/leilux/SICP-exercises/blob/master/book/p216-constraint-propagate(python%20version).py
    布局：
    https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Layout.html#sizes
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
        if Tag.is_container(tag):
            node = self._container_tag_enter(tag, attrs, for_scope)
        elif Tag.is_leaf(tag):
            node = self._leaf_tag_enter(tag, attrs, for_scope)
        else:
            node = self._html_tag_enter(tag, attrs)
            # raise Exception(f"tag '{tag}' not support.")
        return node

    def _gen_widget(self, node, for_scope=None):
        tag = node['tag']
        if Tag.is_container(tag):
            widget = self._container_tag_exit(node, for_scope)
        elif Tag.is_leaf(tag):
            widget = self._leaf_tag_exit(node, for_scope)
        else:
            widget = self._html_tag_exit(node, for_scope)

        return widget

    def _widget_factory(self, widget_cls, attrs, scopes, v_model_widget='value'):
        parsed_attr = self._parse_tag_attr(attrs, scopes, v_model_widget)
        if not parsed_attr['v_if']:
            return None

        # compile node
        kwargs = parsed_attr['kwargs']
        v_slot = parsed_attr['v_slot']
        widget = widget_cls(**kwargs)
        if v_slot:
            widget.v_slot = v_slot

        # compile :attr=exp
        def handle_value_change_vm_to_view(widget, attr):
            def warp(vm, val, old_val):
                if val == old_val:
                    return
                setattr(widget, attr, val)
            return warp

        single_binds = parsed_attr[':']
        for attr, exp in single_binds.items():
            update_vm_to_view = handle_value_change_vm_to_view(widget, attr)
            try:
                _value = ast.literal_eval(exp)
                update_vm_to_view(scopes, _value, None)
            except Exception as e:
                _value = get_attr_from_scopes(scopes, exp)
                update_vm_to_view(scopes, _value, None)
                Watcher(scopes, exp, update_vm_to_view)

        # compile v-model
        def handle_value_change_view_to_vm(_scopes, exp):
            def warp(change):
                return set_attr_to_scopes(_scopes, exp, change['new'])
            return warp

        v_model_vm = parsed_attr['v_model']
        if v_model_vm:
            # print(f">> register observe {widget_cls} {v_model_widget} -> {v_model_vm}")
            update_view_to_vm = handle_value_change_view_to_vm(scopes, v_model_vm)
            widget.observe(update_view_to_vm, names=f'{v_model_widget}')
            _value = get_attr_from_scopes(scopes, v_model_vm)
            update_vm_to_view = handle_value_change_vm_to_view(widget, v_model_widget)
            update_vm_to_view(scopes, _value, None)
            Watcher(scopes, v_model_vm, update_vm_to_view)

        # compile @event
        on_event = parsed_attr['on_events']
        for _event, (func_name, args_name) in on_event.items():
            func = getattr(self.vm.methods, func_name)
            if args_name:
                args = []
                for arg_name in args_name:
                    if arg_name[0].isalpha() or arg_name[0] == '_':
                        arg = get_attr_from_scopes(scopes, arg_name)
                    else:
                        arg = ast.literal_eval(arg_name)
                    args.append(arg)
                func = functools.partial(func, *args)
            getattr(widget, f'on_{_event}')(func)

        return widget

    def _parse_tag_attr(self, attrs, scopes, v_model_widget='value'):
        kwargs = {}
        on_event = {}
        single_bind = {}
        v_model_vm = None
        v_slot = None
        v_if = True
        layout = {}

        for attr, value in attrs.items():
            ok = Directive.is_v_if(attr, value)
            if ok:
                # Todo
                v_if = False
                continue
            # :attr=value
            ok, var = Directive.is_single_bound(attr, value)
            if ok:
                single_bind[var] = value
                continue
            # v-model
            ok, model_vm = Directive.is_v_model(attr, value)
            if ok:
                v_model_vm = model_vm
                continue
            # @click
            ok, event, func, args = Directive.is_event(attr, value)
            if ok:
                on_event[event] = (func, args)
                continue
            # TODO 去除不需要的参数
            ok, slot = Directive.is_v_slot(attr, value)
            if ok:
                v_slot = slot
                continue

            ok = Directive.is_layout(attr, value)
            if ok:
                layout[attr] = value
                continue

            kwargs[attr] = value

        if layout:
            kwargs['layout'] = layout

        return {
            'v_if': v_if,
            ':': single_bind,
            'kwargs': kwargs,
            'on_events': on_event,
            'v_model': v_model_vm,
            'v_slot': v_slot,
        }

    def _container_tag_enter(self, tag, attrs, for_scope=None):
        ast_node = {"tag": tag, 'attrs': attrs, 'body': []}
        return ast_node

    def _container_tag_exit(self, node, for_scope=None):
        tag = node['tag']
        attrs = node['attrs']
        scopes = [self.vm._data, for_scope] if for_scope else [self.vm._data]
        parsed_attr = self._parse_tag_attr(attrs, scopes)

        # TODO can move to Tag class
        widget_cls = Tag.impl(tag)
        if tag == Tag.AppLayout.lower():
            kwargs = parsed_attr.get('kwargs', {})
            for child in node['body']:
                kwargs[child.v_slot] = child
            widget = widget_cls(**kwargs)
        elif tag == Tag.Box.lower() or tag == Tag.HBox.lower():
            widget = widget_cls(node['body'])
        elif tag == Tag.Template.lower():
            widget = widget_cls(node['body'])
        else:
            raise Exception(f'error: container_tag_exit, {tag} not support.')

        v_slot = parsed_attr.get('v_slot')
        if v_slot:
            widget.v_slot = v_slot

        return widget

    def _leaf_tag_enter(self, tag, attrs, for_scope=None):
        ast_node = {"tag": tag, 'attrs': attrs}
        return ast_node

    def _leaf_tag_exit(self, node, for_scope: ForScope = None):
        tag = node['tag']
        scopes = [self.vm._data, for_scope] if for_scope else [self.vm._data]
        return self._widget_factory(Tag.impl(tag), node['attrs'], scopes, Tag.v_model(tag))

    def _html_tag_enter(self, tag, attrs):
        ast_node = {'type': 'html', 'tag': tag, 'attrs': attrs, 'body': []}
        return ast_node

    def _html_tag_exit(self, node, for_scope: ForScope = None):
        body = []
        for child in node['body']:
            if isinstance(child, widgets.HTML):
                body.append(child.value)
            else:
                body.append(child)
        tag = node['tag']
        attr = ' '.join([f"{k}='{v}'" for k, v in node['attrs'].items()])
        html = f"<{tag} {attr}>{' '.join(body)}</{tag}>"
        widget = widgets.HTML(html)
        return widget

    def _for_stmt_enter(self, for_stmt: VForStatement, tag, attrs, is_body):
        body = []
        for i, target in enumerate(getattr(self.vm, for_stmt.iter)):
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
        # v_for_stmt = v_for_ast_node['v_for']
        v_for_stmt = self.v_for_stack[-1]
        _iter = getattr(self.vm, v_for_stmt.iter)
        for i, target in enumerate(_iter):
            # for_scope = (v_for_stmt.i, i, v_for_stmt.target, target, v_for_stmt.target)
            for_scope = ForScope(i, v_for_stmt, self.vm)
            node = v_for_ast_node['body'][i]
            widget = self._gen_widget(node, for_scope)
            if widget:
                _widgets.append(widget)

        # todo 加到v-for的解析处
        if not is_body:
            list_base_dict, attr = get_base_from_scopes([self.vm._data], v_for_stmt.iter)
            # 处理list被整个替换的情况
            list_base_dict.add_dep(attr, ListWatcher(self.vm, f"{attr}: {v_for_stmt.iter} replace"))
            # 处理list本身的变化，append、pop等操作
            list_base = get_attr(list_base_dict, attr)
            list_base.add_dep(ListWatcher(self.vm, f"{v_for_stmt.iter} modified"))

        return _widgets

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        v_for_stmt = attrs.pop(Directive.v_for, None)
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
        def update_text(scopes, for_idx):
            def warp(match):
                exp = match.group(1)
                val = get_attr_from_scopes(scopes, exp)
                attr_base, attr = get_base_from_scopes(scopes, exp)
                attr_base.add_dep(attr, ListWatcher(self.vm, f'html {for_idx} {{{{ {exp} }}}}'))
                return str(val)
            return warp

        if not self.parent_node_stack:
            return

        parent = self.parent_node_stack[-1]
        exp_pattern = r"\{\{\s*(.*?)\s*\}\}"
        if not self.is_in_for_stmt:
            if parent.get('type') == 'html':
                scopes = [self.vm._data]
                result = re.sub(exp_pattern, update_text(scopes, -1), data)
                parent['body'].append(result)
            return

        # TODO node的类型判断可以优化
        if parent['body'] and parent['body'][0].get('type') == 'html':
            v_for_stmt = self.v_for_stack[-1]
            _iter = getattr(self.vm, v_for_stmt.iter)
            for i, target in enumerate(_iter):
                for_scope = ForScope(i, v_for_stmt, self.vm)
                scopes = [self.vm._data, for_scope]
                result = re.sub(exp_pattern, update_text(scopes, i), data)
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
        self.methods = options.get('methods', {})
        self.template = options.get('template')

        self.before_create = options.get('before_create')
        self.created = options.get('created')
        self.before_mount = options.get('before_mount')
        self.mounted = options.get('mounted')
        self.before_update = options.get('before_update ')
        self.updated = options.get('updated ')
        self.render = options.get('render')


def _get_attr(scope, exp, default=None):
    attr_chain = exp.split('.')
    data = scope
    for attr in attr_chain:
        # TODO 可以用自定义的Nil替代，区分值为None的情况
        if isinstance(data, dict):
            data = data.get(attr, default)
        else:
            data = getattr(data, attr, default)
    return data


def get_attr_from_for_scope(scope: 'ForScope', exp: str, default=None):
    attr_split = exp.split('.', 1)
    if len(attr_split) == 1:
        attr_base, attrs = exp, ''
    else:
        attr_base, attrs = attr_split

    if attr_base == scope.for_stmt.iter:
        data_base = scope.iter
    elif attr_base == scope.for_stmt.target:
        data_base = scope.target
    elif attr_base == scope.for_stmt.i:
        return scope.i
    else:
        raise Exception(f"get {exp} from {scope} failed")

    if attrs:
        data = _get_attr(data_base, attrs, default)
    else:
        data = data_base
    return data


def get_attr(scope, exp, default=None):
    if isinstance(scope, ForScope):
        return get_attr_from_for_scope(scope, exp, default)
    return _get_attr(scope, exp, default)


def set_attr(scope, exp: str, value, reactive=False):
    attrs = exp.rsplit('.', 1)
    if len(attrs) == 1:
        attr_set = attrs[0]
        data = scope
    else:
        _attr_get, attr_set = attrs
        data = get_attr(scope, _attr_get)

    if data is None:
        return False

    if reactive:
        setattr(data, attr_set, value)
    else:
        if isinstance(data, Vue):
            data._data[attr_set] = value
        else:
            data[attr_set] = value

    return True


def get_base_from_scope(scope, exp):
    attrs = exp.rsplit('.', 1)
    if len(attrs) == 1:
        return scope, exp
    else:
        attr_base, attr = attrs
        return _get_attr(scope, attr_base), attr


def get_base_from_for_scope(scope: 'ForScope', exp):
    attr_split = exp.split('.', 1)
    if len(attr_split) == 1:
        attr_base, attrs = exp, ''
    else:
        attr_base, attrs = attr_split

    if attr_base == scope.for_stmt.target:
        data_base = scope.target
    else:
        raise Exception(f"get base {exp} from {scope} failed")

    if attrs:
        return get_base_from_scope(data_base, attrs)
    else:
        raise Exception(f"get base {exp} from {scope} failed")


def get_base_from_scopes(scopes, exp):
    for scope in scopes[::-1]:
        try:
            if isinstance(scope, ForScope):
                return get_base_from_for_scope(scope, exp)
            else:
                return get_base_from_scope(scope, exp)
        except Exception:
            pass
    else:
        raise Exception(f"get base {exp} from {scopes} failed")


def get_attr_from_scopes(scopes, exp):
    for scope in scopes[::-1]:
        try:
            data = get_attr(scope, exp)
            if data is not None:
                return data
        except Exception:
            pass
    else:
        raise Exception(f"get attr {exp} from {scopes} failed")


def set_attr_to_scopes(scopes, exp, value, reactive=False):
    for scope in scopes[::-1]:
        if set_attr(scope, exp, value, reactive):
            return True
    return False


class Vue:
    def __init__(self, options, debug=False):
        options = VueOptions(options)
        self._data = observe(options.data)
        self.debug_log = widgets.Output()
        self.debug = debug

        self.dom = None
        self.options = options
        self._call_if_callable(self.options.before_create)
        self._call_if_callable(self.options.created)

        self.methods = self.options.methods(self)
        self._proxy_methods()

        self.mount(self.options.el)

    def log(self, msg):
        if not self.debug:
            return

        with self.debug_log:
            print(msg)

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
        # for func_name, func in self.options.methods.items():
        #     # TODO 绑定self
        #     # setattr(self, func_name, )
        #     pass

    def mount(self, el):
        self._call_if_callable(self.options.before_mount)
        self.render()
        self._call_if_callable(self.options.mounted)

    def _compile_template(self, template):
        vue_template = VueTemplate(self)
        return vue_template.compile(template)

    def render(self):
        self._data = observe(self._data)
        with self.options.el:
            if callable(self.options.template):
                self.dom = self.options.template(self)
            else:
                self.dom = self._compile_template(self.options.template)
            clear_output(True)
            display(self.dom)
