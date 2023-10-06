#!coding: utf-8
import ast
import functools
import re
from html.parser import HTMLParser

import ipywidgets as widgets
import markdown
from IPython.display import clear_output
from IPython.display import display

from observe import observe, Watcher


class MarkdownViewer(widgets.HTML):
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
    HBox = "HBox".lower()
    FloatSlider = "FloatSlider".lower()
    Dropdown = "Dropdown".lower()
    Textarea = "Textarea".lower()
    Button = 'Button'.lower()
    MarkdownViewer = 'MarkdownViewer'.lower()
    Template = 'template'

    container_tags = (AppLayout, Box, HBox, Template)
    leaf_tags = (FloatSlider, Dropdown, Textarea, Button, MarkdownViewer)

    @classmethod
    def is_container(cls, t):
        return t in [i.lower() for i in cls.container_tags]

    @classmethod
    def is_leaf(cls, t):
        return t in [i.lower() for i in cls.leaf_tags]

    @classmethod
    def get_widget(cls, t):
        return getattr(widgets, getattr(cls, t))


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

        kwargs = parsed_attr['kwargs']
        on_event = parsed_attr['on_events']
        v_model_vm = parsed_attr['v_model']
        v_slot = parsed_attr['v_slot']
        widget = widget_cls(**kwargs)
        if v_slot:
            widget.v_slot = v_slot

        # process directive
        def handle_value_change(_scopes, exp):
            def warp(change):
                return set_attr_to_scopes(_scopes, exp, change['new'])
            return warp

        if v_model_vm:
            # print(f">> register observe {widget_cls} {v_model_widget} -> {v_model_vm}")
            widget.observe(handle_value_change(scopes, v_model_vm), names=f'{v_model_widget}')

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
                try:
                    _value = ast.literal_eval(value)
                    kwargs[var] = _value
                    continue
                except Exception as e:
                    self.vm.log(f"warning: parse attr {attr}={value} failed, {e}")
                    pass
                kwargs[var] = get_attr_from_scopes(scopes, value)
                continue
            # v-model
            ok, model_vm = Directive.is_v_model(attr, value)
            if ok:
                v_model_vm = model_vm
                # print(f'>> get v-model {widget_cls} {v_model_widget} ot {v_model_vm}')
                kwargs[v_model_widget] = get_attr_from_scopes(scopes, v_model_vm)
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
        widgets_map = {
            Tag.AppLayout: widgets.AppLayout,
            Tag.Box: widgets.Box,
            Tag.HBox: widgets.HBox,
            Tag.Template: widgets.VBox,
        }

        scopes = [self.vm, for_scope]
        parsed_attr = self._parse_tag_attr(attrs, scopes)

        if tag == Tag.AppLayout.lower():
            kwargs = parsed_attr.get('kwargs', {})
            for child in node['body']:
                kwargs[child.v_slot] = child
            widget = widgets_map[tag](**kwargs)
        elif tag == Tag.Box.lower() or tag == Tag.HBox.lower():
            widget = widgets_map[tag](node['body'])
        elif tag == Tag.Template.lower():
            widget = widgets_map[tag](node['body'])
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
        scopes = [self.vm]
        if for_scope:
            scopes.append(for_scope)

        widgets_map = {
            Tag.FloatSlider: widgets.FloatSlider,
            Tag.Dropdown: widgets.Dropdown,
            Tag.Button: widgets.Button,
            Tag.Textarea: widgets.Textarea,
            Tag.MarkdownViewer: MarkdownViewer,
        }
        v_model_widget = 'value'
        if tag == Tag.Button:
            v_model_widget = 'description'

        return self._widget_factory(widgets_map[tag], node['attrs'], scopes, v_model_widget)

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
        if not self.parent_node_stack:
            return

        parent = self.parent_node_stack[-1]
        if parent.get('type') == 'html':
            parent['body'].append(data)

    # def get_starttag_text(self) -> str | None:
    #     print('starttag', super().get_starttag_text())

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


class ReactiveField:
    def __init__(self, field_name, data):
        self.field_name = field_name
        self._data = data

    def __get__(self, instance, owner):
        return self._data[self.field_name]

    def __set__(self, instance: 'Vue', new_value):
        self._data[self.field_name] = new_value

        instance._call_if_callable(instance.options.before_update)
        instance.render()
        instance._call_if_callable(instance.options.updated)


class Dict(dict):
    pass


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


def get_attr_from_scopes(scopes, exp):
    for scope in scopes[::-1]:
        data = get_attr(scope, exp)
        if data is not None:
            return data


def set_attr_to_scopes(scopes, exp, value, reactive=False):
    for scope in scopes[::-1]:
        if set_attr(scope, exp, value, reactive):
            return True
    return False


class Vue:
    def __init__(self, options):
        self.debug_log = widgets.Output()

        self.dom = None
        self.options = VueOptions(options)
        self._call_if_callable(self.options.before_create)
        self._data = self.options.data
        self._call_if_callable(self.options.created)
        observe(self._data)

        self._proxy_data()
        self.methods = self.options.methods(self)
        self._proxy_methods()

        self.mount(self.options.el)

    def log(self, msg):
        with self.debug_log:
            print(msg)

    def _call_if_callable(self, func):
        if callable(func):
            func(self)

    # TODO 全部代理
    def _proxy_data(self):
        for key, value in self._data.items():
            if isinstance(value, dict):
                item = Dict(value)
                setattr(self.__class__, key, ReactiveField(key, self._data))
                for sub_key, sub_value in value.items():
                    # sub_self = self._data[key]
                    # setattr(sub_self.__class__, sub_key, ReactiveField(sub_key, self._data[key]))
                    setattr(item.__class__, sub_key, ReactiveField(sub_key, item))
                self._data[key] = item
            elif isinstance(value, list) and isinstance(value[0], dict):
                for i, item in enumerate(value):
                    item = Dict(item)
                    for sub_key, sub_value in item.items():
                        setattr(item.__class__, sub_key, ReactiveField(sub_key, item))
                    value[i] = item
                # TODO 响应式的list
                setattr(self.__class__, key, value)
            else:
                setattr(self.__class__, key, ReactiveField(key, self._data))

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
        # clear_output()
        with self.options.el:
            if callable(self.options.template):
                self.dom = self.options.template(self)
            else:
                self.dom = self._compile_template(self.options.template)

            clear_output(True)
            display(self.dom)
