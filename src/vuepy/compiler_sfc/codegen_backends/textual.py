from __future__ import annotations

from enum import Enum
import re
from types import MethodType
from typing import Callable, Dict, Type, TypeVar

from vuepy.compiler_sfc.sfc_codegen import SFC

try:
    from textual.widget import Widget
    from textual.widgets.option_list import Option as OptionItem
    from textual.widgets.selection_list import Selection as SelectionItem
    from textual.app import App
    from textual.containers import VerticalScroll, Vertical
    from textual.widgets import Static
    from textual.screen import Screen
except ImportError as e:
    err_msg = f"{e}, Textual is not installed. " \
              f"Please install it with `pip install textual`."
    print(err_msg)
    raise ImportError(err_msg) from e

from vuepy import VueComponent
from vuepy.compiler_sfc.codegen_backends import TEXTUAL_BACKEND
from vuepy.compiler_sfc.codegen_backends.backend import ICodegenBackend
from vuepy.compiler_sfc.codegen_backends.backend import IDocumentNode
from vuepy.compiler_sfc.codegen_backends.backend import IHTMLNode
from vuepy.compiler_sfc.codegen_backends.backend import INode
from vuepy.compiler_sfc.codegen_backends.backend import ISFCNode
from vuepy.runtime.core.api_setup_helpers import DefineProp, defineEmits


class TextualProvides(Enum):
    APP_MIXIN = 'APP_MIXIN'


_TEXTUAL_WIDGET_TYPES = (Widget, OptionItem, SelectionItem)
TextualWidget = TypeVar('TextualWidget', bound=Widget)

TextualDocBodyWidget = Vertical
TextualHTMLWidget = Static

class TextualRootWidget(VerticalScroll):
    DEFAULT_CSS = """
    TextualRootWidget {
        width: auto;
        height: auto;
    }
    """

class CollectionRootWidget(VerticalScroll):
    DEFAULT_CSS = """
    CollectionRootWidget {
        width: auto;
        height: auto;
    }
    """

class VOnEventMixin:
    """
    @event='xxx' support: keyup, keydown, click, mouse_move, mouse_up, mouse_down, ...
    """

    def action_vp_keyup(self, key, *args):
        cb = self._on_keyup_cb[key]
        cb(*args)

    def vp_register_on_keyup(self, key, cb):
        if not hasattr(self, '_on_keyup_cb'):
            self._on_keyup_cb = {}
        self._on_keyup_cb[key] = cb
        # bind key will trigger action_vp_keyup(key)
        self.bind(key, f"vp_keyup('{key}')", description=cb.__doc__ or '-') #, key_display='xxx')
        # self.refresh_bindings()

    def vp_register_on(self, event: str, cb):
        """
        dynamic create on_{event} function for textual widget
        event: click, mouse_move, mouse_up, mouse_down, ...
        """
        # todo add event check
        on_event_func_name = f"on_{event}"
        event_handler_func_name = f"_vp_{event}_handler"

        def on_event_func(this, event):
            if hasattr(this, event_handler_func_name):
                return getattr(this, event_handler_func_name)(event)

        if not hasattr(self, on_event_func_name):
            setattr(self.__class__, on_event_func_name, on_event_func)

        def event_handler(this, event):
            return cb(event)

        setattr(self, event_handler_func_name, MethodType(event_handler, self))


# todo _WidgetMixin
class TextualDocRootWidget(App, VOnEventMixin):
    MODES = {
        'default_body': 'default_body',
    }

    BINDINGS = [
        # ('x', 'vp_keyup("x")', 'D'),  # for example
    ]

    def __init__(self, *args, **kwargs):
        self._on_mount = []
        if 'css' in kwargs:
            self.CSS = kwargs.pop('css')
        if 'css_path' in kwargs:
            self.CSS_PATH = kwargs.pop('css_path')

        super().__init__(*args, **kwargs)
        self.message_ = ''

    def set_on_mount(self, cb: Callable[[TextualDocRootWidget], None]):
        self._on_mount.append(cb)

    def on_mount(self):
        for cb in self._on_mount:
            cb(self)
    
    def _print_dom_tree(self, widget, indent=0, s='', show_styles=False):
        """recursive print DOM tree structure"""
        indent_str = "  " * indent
        widget_id = f" (id={widget.id})" if widget.id else ""
        widget_classes = f" [classes={widget.classes}]" if widget.classes else ""
        widget_styles = f" [styles={widget.styles}]" if widget.styles and show_styles else ""

        s += f"{indent_str}{widget.__class__.__name__}{widget_id}{widget_classes}{widget_styles}\n"

        for child in widget.children:
            s = self._print_dom_tree(child, indent + 1, s, show_styles)

        return s

    def print_dom_tree(self, widget=None, show_styles=False):
        """print DOM tree structure"""
        if widget is None:
            widget = self
        s = self._print_dom_tree(widget, show_styles=show_styles)
        print(s)
    
    # def action_keyup(self, key, *args):
    #     cb = self._on_keyup[key]
    #     cb(*args)
    
    # def register_on_keyup(self, key, cb):
    #     self._on_keyup_cb[key] = cb
    #     self.bind(key, f"keyup('{key}')", description=cb.__doc__, key_display=cb.__name__)

    # def on_mouse_down(self, event: events.MouseEvent) -> None:
    #     self.screen.query_one(tt_widgets.Log).write(f"{event}\n")

    def exit(
        self,
        result = None,
        return_code: int = 0,
        message = None,
    ) -> None:
        self.message_ = message
        super().exit(result, return_code, message)

    # def on_ready(self) -> None:
    #     self.push_screen(Screen()) 


class TextualNode(INode[TextualWidget]):
    """
    TextualNode is a node that represents a **textual widget**.
    """
    ATTR_MAP = {
        'class': 'classes',
    }

    def __init__(self, widget, *args, app=None, **kwargs):
        self._widget = widget
        self._app = app
    
    def _keyup_vue_to_textual(self, keys_str):
        keys = keys_str.split('.')
        pattern = re.compile(r'^shift\.[a-z]$')
        if pattern.match(keys_str):
            keys = [keys[1].upper()]
        return '+'.join(keys)

    def on(self, ev: str, cb: Callable, remove=False):
        if ev.startswith('keyup.'):
            # ev = ev[6:].replace('.', '+')
            ev = self._keyup_vue_to_textual(ev.replace('keyup.', ''))
            return self._widget.vp_register_on_keyup(ev, cb)

        func_name = f"register_on_{ev}"
        on_event = getattr(self._widget, func_name, None)
        if on_event:
            return on_event(cb)

        # on_mouse_up, on_mouse_down, ...
        if hasattr(self._widget, 'vp_register_on'):
            return self._widget.vp_register_on(ev, cb)
 
        raise AttributeError(f"{func_name} not found in {self._widget}")


    def emit(self, event, *args, **kwargs):
        raise NotImplementedError("emit not supported in textual")

    def observe(self, callback, attr: str = None, remove=False):
        # self._app.document.observe(self._widget, attr, callback, remove)
        self._widget.observe(attr, callback)
        # print(self._app.document.unwrap())
        # self._app.document.unwrap().watch(self.unwrap(), attr, lambda v: callback(v))

    @classmethod
    def convert_to_widget(cls, node) -> TextualWidget:
        w = node.unwrap() if isinstance(node, INode) else node
        if isinstance(w, _TEXTUAL_WIDGET_TYPES):
            return w
        return Static(str(w))

    @property
    def children(self):
        return getattr(self._widget, 'children', [])

    def append(self, *children):
        _children = [self.convert_to_widget(c) for c in children]
        print(self._widget)
        await_mount = self._widget.mount(*_children)
        return await_mount

    def prepend_child(self, child):
        _child = self.convert_to_widget(child)
        # self._widget.mount(_child, before=self._widget.children[0] if self._widget.children else None)
        await_mount = self._widget.mount(_child, before=self.children[0] if self.children else None)
        return await_mount

    def _clear_children(self):
        await_remove = self._widget.remove_children()
        return await_remove

    def replace_children(self, children):
        self._clear_children()
        _children = [self.convert_to_widget(c) for c in children]
        await_mount = self._widget.mount(*_children)
        return await_mount

    @property
    def inner_html(self):
        html = []
        for child in self.children:
            if isinstance(child, TextualHTMLWidget):
                html.append(child.render())
        return '\n'.join(html)

    def setattr(self, name, value):
        name = self.ATTR_MAP.get(name, name)
        setattr(self._widget, name, value)

    def getattr(self, name, *default):
        if len(default) > 1:
            raise TypeError(f'getattr expected at most 3 arguments, got {len(default)}')
        if len(default) == 1:
            return getattr(self._widget, name, default[0])
        else:
            return getattr(self._widget, name)

    def hasattr(self, name: str) -> bool:
        return hasattr(self._widget, name)


class TextualSFCNode(
    ISFCNode[TextualRootWidget],
    TextualNode[TextualRootWidget],
):
    """
    TextualSFCNode is a node that represents a **SFC widget from .vue file**.
    """
    def __init__(
        self,
        props: Dict[str, DefineProp],
        emitter: defineEmits,
        sfc: SFC,
        is_root_component: bool = False
    ):
        self._id = f'sfc-{id(self)}'
        if is_root_component:
            self._id = "sfc-root"

        self.cls = TextualRootWidget
        if (not is_root_component) and sfc.style_str:
            self.cls = type(
                f'_SFCRootWidget_{id(self)}',
                (TextualRootWidget,),
                {
                    'DEFAULT_CSS': sfc.style_str,
                }
            )

        fallthrough_attrs = {
            key: value for key, value in sfc._context.get('attrs', {}).items() if key not in props
        }
        if 'class' in fallthrough_attrs:
            fallthrough_attrs['classes'] = fallthrough_attrs.pop('class')
        self._fallthrough_attrs = {'id': self._id, **fallthrough_attrs}

        widget = self.cls(**self._fallthrough_attrs)
        super().__init__(widget, props, emitter, sfc, is_root_component)
    
    def create_widget(self, children):
        _children = [self.convert_to_widget(c) for c in children]
        self._widget = self.cls(*_children, **self._fallthrough_attrs)


TextualDocBodyWidget = Screen

class TextualDocumentNode(
    IDocumentNode[TextualDocRootWidget, TextualDocBodyWidget],
    TextualNode[TextualDocRootWidget],
):
    def __init__(self, root: TextualDocRootWidget = None, body_node: TextualDocBodyWidget = None, *args, **kwargs):
        root_widget = root or TextualDocRootWidget()
        body_node = body_node or TextualDocBodyWidget(id="default_body")
        if not isinstance(body_node, TextualNode):
            body_node = TextualNode(body_node)
        super().__init__(root_widget, body_node, *args, **kwargs)
    
    def add_body(self, body):
        self.body = body
        def on_mount(app):
            app.install_screen(body.unwrap(), name='default_body')
            app.switch_mode('default_body')

        self._widget.set_on_mount(on_mount)
        # self._widget.push_screen(body.unwrap())


class TextualNodeCollection(TextualNode[CollectionRootWidget]):
    def __init__(self, widget=None, kind: str = "collection", *args, **kwargs):
        if not widget:
            children = kwargs.pop('children', [])
            _children = [self.convert_to_widget(c) for c in children]
            widget = CollectionRootWidget(*_children, id=f'{kind}-{id(self)}')

        super().__init__(widget, *args, **kwargs)


class TextualHTMLNode(
    IHTMLNode[TextualHTMLWidget],
    TextualNode[TextualHTMLWidget],
):
    def __init__(self, widget=None, value=None, *args, **kwargs):
        widget = widget or TextualHTMLWidget(value or "", **kwargs)
        if not isinstance(widget, TextualHTMLWidget):
            raise ValueError(f"widget {widget} should be {TextualHTMLWidget}")
        super().__init__(widget, *args, **kwargs)
        self._vp_change_callbacks = []

    @property
    def outer_html(self):
        # return self._widget.render()
        return self._widget.content

    @outer_html.setter
    def outer_html(self, val):
        # Trigger change callbacks if value changed
        self._widget.update(val)
        if self._vp_change_callbacks:
            for callback in self._vp_change_callbacks:
                try:
                    callback({'new': val})
                except TypeError:
                    # If callback doesn't accept dict, pass value directly
                    callback(val)

    def on_change(self, callback, remove=False):
        if remove:
            if callback in self._vp_change_callbacks:
                self._vp_change_callbacks.remove(callback)
        else:
            self._vp_change_callbacks.append(callback)


class TextualCodegenBackend(ICodegenBackend):
    """
    textual codegen backend
    """
    NAME = TEXTUAL_BACKEND
    ESCAPE_MUSTACHE_TEXT = False

    @classmethod
    def get_template_component(cls) -> Type[VueComponent]:
        from textual_vuepy.comps import VBox
        from functools import partial
        # return partial(VBox, id='template')
        return VBox

    @classmethod
    def gen_widget_collection_node(
        cls,
        children=None,
        kind: str = "collection",
    ) -> "TextualNodeCollection":
        return TextualNodeCollection(children=children, kind=kind)

    @classmethod
    def gen_sfc_widget_node(
        cls,
        props: Dict[str, DefineProp],
        emitter: defineEmits,
        sfc: SFC,
        is_root: bool = False,
    ) -> TextualSFCNode:
        return TextualSFCNode(props, emitter, sfc, is_root)

    @classmethod
    def gen_document_node(cls, vue_root) -> TextualDocumentNode:
        app_mixin = (
            vue_root.app.inject(TextualProvides.APP_MIXIN)
            or vue_root.app.inject(TextualProvides.APP_MIXIN.value)
        )
        _TextualDocRootWidget = TextualDocRootWidget
        if app_mixin:
            _TextualDocRootWidget = type(
                f"TextualDocRootWidget_{app_mixin.__name__}_{id(vue_root)}",
                (app_mixin, TextualDocRootWidget),
                {}
            )

        root_widget = _TextualDocRootWidget(
            css=vue_root.style_str, 
            css_path=vue_root.style_src,
        )
        return TextualDocumentNode(root_widget)

    @classmethod
    def gen_html_node(cls) -> TextualHTMLNode:
        return TextualHTMLNode()
    
    @classmethod
    def is_servable(cls) -> bool:
        # textual's web service is completed by `vuepy run --servable` 
        # (cli/run_vue.py + textual-serve), not by App.mount
        return False
