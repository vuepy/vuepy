# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

import abc
from abc import ABC
from typing import Dict
from typing import Iterable
from typing import List
from typing import Tuple

from ipywui.core import has_and_pop
from vuepy import App
from vuepy import VueComponent
from vuepy.compiler_sfc.codegen_backends.backend import IHTMLNode
from vuepy.compiler_sfc.codegen_backends.textual import TextualNode
from vuepy.compiler_sfc.codegen_backends.textual import TextualWidget
from vuepy.runtime.core.api_create_app import VuePlugin
from vuepy.utils.factory import FactoryMeta

_NAMESPACE = ''


class vtextual(VuePlugin, metaclass=FactoryMeta):
    @classmethod
    def install(cls, app: App, options: dict):
        # textual does not require extension loading like panel
        components = cls.get_all_registry()
        for name, component in components.items():
            app.component(name, component)

        app.message = app.document.unwrap().notify

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


class VTextualComponent(VueComponent, ABC):
    _PARAMS_STORE_TRUE: List[Tuple[str, bool]] = [
        ('disabled', False),
        ('compact', False),
    ]
    PARAMS_STORE_TRUE: List[Tuple[str, bool]] = []
    TextualNodeClass: TextualNode = TextualNode

    WIDGET_ATTRS = [
        'style',
        'border_title',
        'border_subtitle',
    ]
    CONTENT_SLOT: tuple[str, str] = None # ('default', 'content')

    def _process_store_true_params(self, attrs, props):
        params = {}
        for key, default in self._PARAMS_STORE_TRUE + self.PARAMS_STORE_TRUE:
            if key in attrs:
                params[key] = attrs.pop(key) != False
            elif key in props:
                params[key] = props.pop(key) != False
            
        return params

    def _convert_slot_nodes_to_widgets(self, slots: Dict | None):
        if not slots:
            return
        for name, children in slots.items():
            if isinstance(children, Iterable):
                children = [TextualNode.convert_to_widget(child) for child in children]
            else:
                children = TextualNode.convert_to_widget(children)
            slots[name] = children

    def _convert_class_to_classes(self, kw):
        classes = kw.pop('class', None)
        if not classes:
            return
        kw['classes'] = classes

    def _process_postset_attrs(self, attrs, props):
        _attrs = {}
        for attr in self.WIDGET_ATTRS:
            if attr in attrs:
                _attrs[attr] = attrs.pop(attr)
            elif attr in props:
                _attrs[attr] = props.pop(attr)
        return _attrs

    def render(self, ctx, props, setup_returned) -> TextualNode:
        attrs = ctx.get('attrs', {})
        params = self._process_store_true_params(attrs, props)

        postset_attrs = self._process_postset_attrs(attrs, props)
        self._convert_class_to_classes(attrs)
        self._convert_class_to_classes(props)
        content_slot_node = None
        if self.CONTENT_SLOT:
            slot_name, content_attr = self.CONTENT_SLOT
            content_slot = ctx.get('slots', {}).get(slot_name, [])
            content_slot_node: IHTMLNode = content_slot[0] if content_slot else None
            if content_slot_node:
                attrs[content_attr] = content_slot_node.outer_html

        self._convert_slot_nodes_to_widgets(ctx.get('slots'))

        widget = self._render(ctx, attrs, props, params, setup_returned)

        if content_slot_node:
            def _update_attr(change):
                val = change['new'] if isinstance(change, dict) else change
                setattr(widget, content_attr, val)

            content_slot_node.on_change(_update_attr)

        # post create
        for attr, value in postset_attrs.items():
            setattr(widget, attr, value)

        return self.TextualNodeClass(widget, app=ctx.get('app'))

    @abc.abstractmethod
    def _render(self, ctx, attrs, props, params, setup_returned) -> TextualWidget:
        raise NotImplementedError
