from __future__ import annotations

from typing import Awaitable
from typing import Callable
from typing import Dict
from typing import Type
from typing import TypeVar
from typing import Union

try:
    from panel.viewable import ServableMixin
    from panel.viewable import Viewable
    import panel as pn
    import param
except ImportError as e:
    err_msg = f"{e}, Panel is not installed. " \
              f"Please install it with `pip install panel ipywidgets_bokeh`."
    print(err_msg)
    raise ImportError(err_msg) from e

from vuepy import VueComponent
from vuepy.compiler_sfc.codegen_backends.backend import ICodegenBackend
from vuepy.compiler_sfc.codegen_backends.backend import IDocumentNode
from vuepy.compiler_sfc.codegen_backends.backend import IHTMLNode
from vuepy.compiler_sfc.codegen_backends.backend import INode
from vuepy.compiler_sfc.codegen_backends.backend import ISFCNode
from vuepy.runtime.core.api_setup_helpers import DefineProp
from vuepy.runtime.core.api_setup_helpers import defineEmits

_PN_WIDGET_TYPES = (Viewable, ServableMixin)
PnWidget = TypeVar('PnWidget', bound=Union[Viewable, ServableMixin])

SFCRootWidget = pn.Column
DocRootWidget = pn.Column
DocBodyWidget = pn.Column
CollectionRootWidget = pn.Column
HTMLWidget = pn.pane.HTML


class PnNode(INode[PnWidget]):
    def on(
        self, ev: str,
        cb: Callable[[param.parameterized.Event], None | Awaitable[None]],
        remove=False
    ) -> param.parameterized.Watcher:
        """
        """
        func_name = f"on_{ev}"
        on_event = getattr(self._widget, func_name, None)
        if on_event is None:
            raise AttributeError(f"{func_name} not found in {self._widget}")
        return on_event(cb)

    def emit(self, event, *args, **kwargs):
        raise NotImplementedError("emit not supported in panel")

    def observe(self, callback, attr: str = None, remove=False):
        if remove:
            self._widget.param.unwatch(callback, attr)
        else:
            self._widget.param.watch(callback, attr)

    @classmethod
    def convert_to_widget(cls, node) -> PnWidget:
        w = node.unwrap() if isinstance(node, INode) else node
        if isinstance(w, _PN_WIDGET_TYPES):
            return w

        return pn.panel(w)

    @property
    def children(self):
        return self._widget[::]

    def append(self, *children):
        # auto convert
        _children = [self.convert_to_widget(c) for c in children]
        self._widget.extend(_children)

    def prepend_child(self, child):
        # auto convert
        _child = self.convert_to_widget(child)
        self._widget.insert(0, _child)

    def replace_children(self, children):
        # auto convert
        _children = [self.convert_to_widget(c) for c in children]
        if len(_children) == 0:
            self._widget.clear()
        else:
            self._widget[:] = _children

    @property
    def inner_html(self):
        html = []
        for child in self.children:
            if isinstance(child, HTMLWidget):
                html.append(child.object)
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


class PnSFCNode(
    ISFCNode[pn.Column],
    PnNode[SFCRootWidget],
):
    def __init__(
        self,
        props: Dict[str, DefineProp],
        emitter: defineEmits
    ):
        super().__init__(SFCRootWidget(), props, emitter)


class PnDocumentNode(
    IDocumentNode[DocRootWidget, DocBodyWidget],
    PnNode[DocRootWidget],
):
    def __init__(
        self,
        root: DocBodyWidget = None,
        body_node: DocBodyWidget = None,
        *args,
        **kwargs
    ):
        root_widget = root or DocRootWidget(name='root')
        body_node = body_node or DocBodyWidget(name='body')
        if not isinstance(body_node, PnNode):
            body_node = PnNode(body_node)
        super().__init__(root_widget, body_node, *args, **kwargs)


class PnNodeCollection(PnNode[CollectionRootWidget]):
    def __init__(self, widget=None, *args, **kwargs):
        widget = widget or CollectionRootWidget()
        super().__init__(widget, *args, **kwargs)


class PnHTMLNode(
    IHTMLNode[HTMLWidget],
    PnNode[HTMLWidget],
):
    def __init__(self, widget=None, value=None, *args, **kwargs):
        widget = widget or HTMLWidget(value, **kwargs)
        if not isinstance(widget, HTMLWidget):
            raise ValueError(f"widget {widget} should be {HTMLWidget}")
        super().__init__(widget, *args, **kwargs)

    @property
    def outer_html(self):
        return self._widget.object

    @outer_html.setter
    def outer_html(self, val):
        self._widget.object = val

    def on_change(self, callback, remove=False):
        self.observe(callback, 'object', remove)


# instead of lazy_register
class PnCodegenBackend(ICodegenBackend):
    """
    panel codegen backend
    """

    @classmethod
    def get_template_component(cls) -> Type[VueComponent]:
        from panel_vuepy import Column
        return Column

    @classmethod
    def gen_widget_collection_node(cls) -> "PnNodeCollection":
        """
        for dummy, slot node
        """
        return PnNodeCollection()

    @classmethod
    def gen_sfc_widget_node(
        cls,
        props: Dict[str, DefineProp],
        emitter: defineEmits
    ) -> PnSFCNode:
        return PnSFCNode(props, emitter)

    @classmethod
    def gen_document_node(cls) -> PnDocumentNode:
        return PnDocumentNode()

    @classmethod
    def gen_html_node(cls) -> PnHTMLNode:
        return PnHTMLNode()
    
    @classmethod
    def is_servable(cls) -> bool:
        return True
