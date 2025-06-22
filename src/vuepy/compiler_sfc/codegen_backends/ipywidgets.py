from __future__ import annotations

from typing import Dict
from typing import Tuple
from typing import Type
from typing import TypeVar

import anywidget
import ipywidgets as iw

from vuepy import VueComponent
from vuepy.compiler_sfc.codegen_backends import CodegenBackendMgr
from vuepy.compiler_sfc.codegen_backends.backend import ICodegenBackend
from vuepy.compiler_sfc.codegen_backends.backend import IDocumentNode
from vuepy.compiler_sfc.codegen_backends.backend import IHTMLNode
from vuepy.compiler_sfc.codegen_backends.backend import INode
from vuepy.compiler_sfc.codegen_backends.backend import ISFCNode
from vuepy.runtime.core.api_setup_helpers import DefineProp
from vuepy.runtime.core.api_setup_helpers import defineEmits

IwWidget = TypeVar('IwWidget', bound=iw.Widget)

SFCRootWidget = iw.VBox
DocRootWidget = iw.VBox
DocBodyWidget = iw.VBox
HTMLWidget = iw.HTMLMath

NAME = 'ipywidgets'


class IwNode(INode[IwWidget]):
    def on(self, ev: str, cb: callable, remove=False):
        func_name = f"on_{ev}"
        on_event = getattr(self._widget, func_name, None)
        if on_event is None:
            raise AttributeError(f"{func_name} not found in {self._widget}")
        return on_event(cb, remove)

    def emit(self, event, *args, **kwargs):
        raise NotImplementedError("emit not supported in ipywidgets")

    def observe(self, callback, attr: str = None, remove=False):
        if attr is None:
            if remove:
                self._widget.unobserve(callback)
            else:
                self._widget.observe(callback)
        else:
            if remove:
                self._widget.unobserve(callback, names=attr)
            else:
                self._widget.observe(callback, names=attr)

    @classmethod
    def convert_to_widget(cls, node) -> IwWidget:
        w = node.unwrap() if isinstance(node, INode) else node
        iw_support_widgets = (iw.Widget, anywidget.AnyWidget, SFCRootWidget)
        if isinstance(w, iw_support_widgets):
            return w

        try:
            import panel as pn
            return pn.ipywidget(w)
        except Exception as e:
            err_msg = f"convert {w} to ipywidgets failed, {e}, Maybe Panel is not installed. " \
                      f"Please install it with `pip install panel jupyter_bokeh`."
            print(err_msg)
            raise ImportError(err_msg) from e

    @property
    def children(self) -> Tuple[IwWidget]:
        return self._widget.children

    def append(self, *children):
        _children = [self.convert_to_widget(c) for c in children]
        self._widget.children = (*self._widget.children, *_children)

    def prepend_child(self, child):
        self._widget.children = (self.convert_to_widget(child), *self._widget.children)

    def replace_children(self, children):
        _children = tuple(self.convert_to_widget(c) for c in children)
        self._widget.children = _children

    @property
    def inner_html(self):
        html = []
        for child in self.children:
            if isinstance(child, HTMLWidget):
                html.append(child.value)
        return '\n'.join(html)

    def setattr(self, name, value):
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


class IwSFCNode(
    ISFCNode[SFCRootWidget],
    IwNode[SFCRootWidget],
):
    def __init__(
        self,
        props: Dict[str, DefineProp],
        emitter: defineEmits
    ):
        super().__init__(SFCRootWidget(), props, emitter)


class IwDocumentNode(
    IDocumentNode[DocRootWidget, DocBodyWidget],
    IwNode[DocRootWidget],
):
    def __init__(
        self,
        root: DocBodyWidget = None,
        body_node: DocBodyWidget = None,
        *args,
        **kwargs
    ):
        root_widget = root or DocRootWidget()
        body_node = body_node or DocBodyWidget()
        if not isinstance(body_node, IwNode):
            body_node = IwNode(body_node)
        super().__init__(root_widget, body_node, *args, **kwargs)


CollectionRootWidget = iw.VBox


class IwNodeCollection(IwNode[CollectionRootWidget]):
    def __init__(self, widget=None, *args, **kwargs):
        widget = widget or CollectionRootWidget()
        super().__init__(widget, *args, **kwargs)


class IwHTMLNode(
    IHTMLNode[HTMLWidget],
    IwNode[HTMLWidget],
):
    def __init__(self, widget=None, value=None, *args, **kwargs):
        widget = widget or HTMLWidget(value, **kwargs)
        if not isinstance(widget, HTMLWidget):
            raise ValueError(f"widget {widget} should be {HTMLWidget}")
        super().__init__(widget, *args, **kwargs)

    @property
    def outer_html(self):
        return self._widget.value

    @outer_html.setter
    def outer_html(self, val):
        self._widget.value = val

    def on_change(self, callback, remove=False):
        self.observe(callback, 'value', remove)


@CodegenBackendMgr.register(NAME)
class IwCodegenBackend(ICodegenBackend):
    """
    ipywidgets codegen backend
    """

    @classmethod
    def get_template_component(cls) -> Type[VueComponent]:
        from ipywui import Template
        return Template

    @classmethod
    def gen_widget_collection_node(cls) -> "IwNodeCollection":
        """
        for dummy, slot node
        """
        return IwNodeCollection()

    @classmethod
    def gen_sfc_widget_node(
        cls,
        props: Dict[str, DefineProp],
        emitter: defineEmits
    ) -> IwSFCNode:
        return IwSFCNode(props, emitter)

    @classmethod
    def gen_document_node(cls) -> IwDocumentNode:
        return IwDocumentNode()

    @classmethod
    def gen_html_node(cls) -> IwHTMLNode:
        return IwHTMLNode()
