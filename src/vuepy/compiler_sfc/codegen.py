# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

import abc

import ipywidgets as widgets

from vuepy import log

logger = log.getLogger()


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


class SetupContext:
    def __init__(self):
        self.attrs = {}
        self.slots = {}
        # 触发事件
        self.emit = {}
        # 暴露公共属性
        self.expose = {}


class VNode:
    def __init__(self, type_, props, children=None, key=''):
        self.type = type_
        self.props = props
        self.children = children
        self.key = key


class VueComponent(metaclass=abc.ABCMeta):
    _name = ''
    props = {}
    template = ''

    v_model_default = 'value'

    def __init__(self, setup_ret: dict = None, template: str = '', app: "App" = None):
        self.template = template
        self._data: dict = setup_ret
        self.app = app

    @classmethod
    def name(cls):
        # return (cls._name or cls.__name__).lower()
        return cls._name or cls.__name__

    def setup(self, props: dict = None, ctx=None, vm: 'App' = None):
        """

        :param props:
        :param ctx: attrs, slots, emit
        :param vm:
        :return:
        """
        pass

    def component(self, name: str):
        comp = self.to_ns().get(name)
        try:
            from vuepy.compiler_sfc.sfc_codegen import SFCType
            if comp and (isinstance(comp, SFCType) or issubclass(comp, VueComponent)):
                return comp
        except Exception as e:
            logger.debug(f"find component({name}) in Component `{self.name()}` failed, {e}.")
            pass

        comp = self.app.component(name)
        return comp

    def to_ns(self):
        return {
            **self.app.config.globalProperties.to_ns(),
            **self._data,
        }

    def render(self, ctx, props, setup_returned) -> VNode:
        """
        h(tag, props|attrs, children)

        :param ctx: attrs, slots, emit
        :param setup_returned:
        :param props:
        :return:
        """
        # if not self.template:
        #     return None
        # return vue_compiler_dom(self.template)
        pass
