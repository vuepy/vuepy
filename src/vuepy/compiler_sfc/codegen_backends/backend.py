from __future__ import annotations

import enum
from abc import ABC
from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import Generic
from typing import Type
from typing import TypeVar

from vuepy.compiler_sfc.codegen import VueComponent
from vuepy.runtime.core.api_setup_helpers import DefineProp
from vuepy.runtime.core.api_setup_helpers import defineEmits
from vuepy.utils.factory import FactoryMeta


class CodegenBackendMgr(metaclass=FactoryMeta):
    """
    manage codegen backends
    """

    @classmethod
    def register_lazy(cls, name, module_cls_path):
        if name in cls._registry:
            raise ValueError(f"Backend {name} already registered")
        cls._registry[name] = module_cls_path

    @classmethod
    def get_by_name(cls, name):
        backend = cls._registry.get(name, None)
        # lazy load
        if isinstance(backend, str):
            module, backend_cls = backend.rsplit('.', 1)
            module = __import__(module, fromlist=[backend_cls])
            backend = getattr(module, backend_cls)
            cls._registry[name] = backend

        return backend


class ICodegenBackend(metaclass=ABCMeta):
    """
    codegen backend interface
    """

    @classmethod
    def get_template_component(cls) -> Type[VueComponent]:
        raise NotImplementedError

    @classmethod
    def gen_widget_collection_node(cls) -> "INode":
        raise NotImplementedError

    @classmethod
    def gen_sfc_widget_node(
        cls,
        props: Dict[str, DefineProp],
        emitter: defineEmits
    ) -> 'ISFCNode':
        raise NotImplementedError

    @classmethod
    def gen_document_node(cls) -> 'IDocumentNode':
        raise NotImplementedError

    @classmethod
    def gen_html_node(cls) -> 'IHTMLNode':
        raise NotImplementedError
    
    @classmethod
    def is_servable(cls) -> bool:
        return False


W = TypeVar('W')


class INode(Generic[W], ABC):
    """
    node interface, a Widget Proxy

    https://developer.mozilla.org/en-US/docs/Web/API/Node
    https://developer.mozilla.org/en-US/docs/Web/API/Element
    """

    def __init__(self, widget: W, *args, **kwargs):
        self._widget: W = widget

    @abstractmethod
    def on(self, event, callback, remove=False):
        raise NotImplementedError

    @abstractmethod
    def emit(self, event, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def observe(self, callback, attr: str = None, remove=False):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def convert_to_widget(cls, node):
        raise NotImplementedError

    @property
    @abstractmethod
    def children(self):
        raise NotImplementedError

    @children.setter
    def children(self, _children):
        self.replace_children(_children)

    @abstractmethod
    def append(self, *children):
        raise NotImplementedError

    @abstractmethod
    def prepend_child(self, child):
        raise NotImplementedError

    @abstractmethod
    def replace_children(self, children):
        raise NotImplementedError

    @property
    @abstractmethod
    def inner_html(self):
        raise NotImplementedError

    # @inner_html.setter
    # def inner_html(self, val):
    #     pass

    @abstractmethod
    def setattr(self, name: str, value):
        raise NotImplementedError

    @abstractmethod
    def getattr(self, name: str, *default: Any):
        raise NotImplementedError

    @abstractmethod
    def hasattr(self, name: str) -> bool:
        raise NotImplementedError

    def __repr__(self):
        return f"<{self.__class__.__module__}.{self.__class__.__name__}" \
               f"({self._widget!r}) object at {hex(id(self))}>"

    def unwrap(self) -> W:
        return self._widget


class SFCLifeCycle(enum.Enum):
    ON_BEFORE_MOUNT = 'on_before_mount'
    ON_MOUNTED = 'on_mounted'
    ON_BEFORE_UNMOUNT = 'on_before_unmount'
    ON_UNMOUNTED = 'on_unmounted'


class ISFCNode(INode[W], ABC):
    """
    sfc node interface
    """

    def __init__(
        self,
        widget,
        props: Dict[str, DefineProp],
        emitter: defineEmits
    ):
        super().__init__(widget)
        self._emitter = emitter
        self._props = props

    def on(self, event: str | SFCLifeCycle, callback: callable, remove=False):
        # return handler?
        self._emitter.add_event_listener(event, callback, remove)

    def emit(self, event, *args, **kwargs):
        return self._emitter(event, *args, **kwargs)

    def setattr(self, name, value):
        if hasattr(self._widget, name):
            setattr(self._widget, name, value)
        elif name in self._props:
            self._props[name].value = value
        else:
            raise AttributeError(f"Attribute {name} not found in widget or props")

    def getattr(self, name, *default):
        if len(default) > 1:
            raise TypeError(f'getattr expected at most 3 arguments, got {len(default)}')

        if hasattr(self._widget, name):
            return getattr(self._widget, name)
        elif name in self._props:
            return self._props[name].value
        elif len(default) == 1:
            return default[0]
        else:
            # len(default) == 0 raise AttributeError
            return getattr(self._widget, name)


W_ROOT_WIDGET = TypeVar('W_ROOT_WIDGET')
W_BODY_NODE = TypeVar('W_BODY_NODE', bound=INode)


class IDocumentNode(
    Generic[W_ROOT_WIDGET, W_BODY_NODE],
    INode[W_ROOT_WIDGET],
    ABC
):
    """
    document node interface
    https://developer.mozilla.org/en-US/docs/Web/API/Document
    """

    def __init__(
        self,
        root_widget: W_ROOT_WIDGET = None,
        body_node: W_BODY_NODE = None,
        *args,
        **kwargs
    ):
        super().__init__(root_widget, *args, **kwargs)
        self.body = body_node
        if body_node:
            self.add_body(body_node)

    def add_body(self, body: W_BODY_NODE):
        self.body = body
        self.append(body)


class IHTMLNode(INode[W], ABC):
    """
    html node interface
    """

    def __init__(self, widget, *args, **kwargs):
        super().__init__(widget, *args, **kwargs)

    @property
    def outer_html(self):
        raise NotImplementedError

    @outer_html.setter
    def outer_html(self, val):
        raise NotImplementedError

    @abstractmethod
    def on_change(self, callback, remove=False):
        raise NotImplementedError
