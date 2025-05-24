# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import Iterable, List
from typing import Tuple

from ipywui.widgets import WidgetCssStyle
from ipywui.widgets.custom.message import MessageService
from vuepy import App
from vuepy import VueComponent
from vuepy.compiler_sfc.codegen_backends import ipywidgets as iw_backend
from vuepy.compiler_sfc.codegen_backends.ipywidgets import IwNode
from vuepy.compiler_sfc.codegen_backends.ipywidgets import IwWidget
from vuepy.runtime.core.api_create_app import VuePlugin
from vuepy.utils.factory import FactoryMeta


class wui(VuePlugin, metaclass=FactoryMeta):
    @classmethod
    def install(cls, app: "App", options: dict):
        components = cls.get_all_registry()
        for name, component in components.items():
            app.component(name, component)

        app.message = MessageService(app_instance=app)
        # todo panel时如何使用message？
        if app.codegen_backend == iw_backend.NAME:
            app.document.body.prepend_child(app.message.widget)
        # app.document.body_node.appendLeftChild(app.message.widget)


class IPywidgetsComponent(VueComponent, ABC):
    STYLE_ATTR = 'style'
    PARAMS_STORE_TRUE: List[Tuple[str, bool]] = []

    def _process_style(self, kw):
        styles = kw.pop(self.STYLE_ATTR, None)
        if styles:
            kw.update(WidgetCssStyle.convert_css_style_to_widget_style_and_layout(styles))

    def _process_store_true_params(self, attrs, props):
        params = {}
        for key, default in self.PARAMS_STORE_TRUE:
            params[key] = has_and_pop(attrs, key) or has_and_pop(props, key) or default

        return params

    @classmethod
    def name(cls):
        # todo
        # return f'Ipw{cls.__name__}'
        return cls.__name__

    def _convert_slot_nodes_to_widgets(self, slots: Dict | None):
        if not slots:
            return

        for name, children in slots.items():
            if isinstance(children, Iterable):
                children = [IwNode.convert_to_widget(child) for child in children]
            else:
                children = IwNode.convert_to_widget(children)
            slots[name] = children

    def render(self, ctx, props, setup_returned) -> IwNode:
        attrs = ctx.get('attrs', {})
        params = self._process_store_true_params(attrs, props)

        self._process_style(attrs)
        self._process_style(props)

        self._convert_slot_nodes_to_widgets(ctx.get('slots'))
        widget = self._render(ctx, attrs, props, params, setup_returned)
        return IwNode(widget)

    @abstractmethod
    def _render(self, ctx, attrs, props, params, setup_returned) -> IwWidget:
        raise NotImplementedError


def has_and_pop(attrs, key):
    if key in attrs:
        attrs.pop(key)
        return True
    return False


def is_float(n):
    return isinstance(n, float)


def is_int(n):
    return isinstance(n, int)


def is_str(s):
    return isinstance(s, str)


def is_tuple(t):
    return isinstance(t, (tuple, list))
