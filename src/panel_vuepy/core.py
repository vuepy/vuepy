# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

import abc
from abc import ABC
from types import MethodType
from typing import Dict
from typing import Iterable
from typing import List
from typing import Tuple

import panel as pn

from ipywui.core import has_and_pop
from vuepy import App
from vuepy import VueComponent
from vuepy.compiler_sfc.codegen_backends.panel import PnNode
from vuepy.compiler_sfc.codegen_backends.panel import PnWidget
from vuepy.runtime.core.api_create_app import VuePlugin
from vuepy.utils.factory import FactoryMeta

_NAMESPACE = 'Pn'


class vpanel(VuePlugin, metaclass=FactoryMeta):
    @classmethod
    def install(cls, app: App, options: dict):
        pn.extension()

        components = cls.get_all_registry()
        for name, component in components.items():
            app.component(name, component)

    @classmethod
    def ns_register(cls, name=None):
        def _(sub_cls):
            if isinstance(name, (list, tuple)):
                ret = None
                for _name in name:
                    ret = cls.register(_NAMESPACE + _name)(sub_cls)
                return ret
            else:
                _name = name or (sub_cls.name() if callable(sub_cls.name) else sub_cls.name)
                return cls.register(_NAMESPACE + _name)(sub_cls)

        return _


class VPanelComponent(VueComponent, ABC):
    STYLE_ATTR = 'style'
    PARAMS_STORE_TRUE: List[Tuple[str, bool]] = []
    LOAD_EXTENSION = False
    PnNodeClass: PnNode = PnNode

    @classmethod
    def _load_extension(cls):
        pn.extension()

    def _process_style(self, kw):
        css_style = kw.pop(self.STYLE_ATTR, None)
        if not css_style:
            return

        if isinstance(css_style, dict):  # Adaptation :style="{'a': 1}"
            styles = css_style.items()
        else:
            styles = dict(
                kv.strip().split(':', maxsplit=1)
                for kv in css_style.rstrip('; ').split(';')
            )

        kw['styles'] = styles

    def _process_store_true_params(self, attrs, props):
        params = {}
        for key, default in self.PARAMS_STORE_TRUE:
            params[key] = bool(has_and_pop(attrs, key) or has_and_pop(props, key) or default)

        return params

    def _convert_slot_nodes_to_widgets(self, slots: Dict | None):
        if not slots:
            return

        for name, children in slots.items():
            if isinstance(children, Iterable):
                children = [PnNode.convert_to_widget(child) for child in children]
            else:
                children = PnNode.convert_to_widget(children)
            slots[name] = children

    def _inject_on_change_register(self, widget: PnWidget):
        attr = self.v_model_default
        if not hasattr(widget, attr):
            return

        def on_change(this: PnWidget, callback, remove=False):
            if remove:
                this.param.unwatch(callback, attr)
            else:
                this.param.watch(callback, attr)

        setattr(widget, 'on_change', MethodType(on_change, widget))

    def render(self, ctx, props, setup_returned) -> PnNode:
        if not self.LOAD_EXTENSION:
            self._load_extension()
            self.LOAD_EXTENSION = True

        attrs = ctx.get('attrs', {})
        params = self._process_store_true_params(attrs, props)
        # process style
        self._process_style(attrs)
        self._process_style(props)

        # process slots
        self._convert_slot_nodes_to_widgets(ctx.get('slots'))
        widget = self._render(ctx, attrs, props, params, setup_returned)

        # Inject on_change support
        self._inject_on_change_register(widget)

        return self.PnNodeClass(widget)

    @abc.abstractmethod
    def _render(self, ctx, attrs, props, params, setup_returned) -> PnWidget:
        raise NotImplementedError
