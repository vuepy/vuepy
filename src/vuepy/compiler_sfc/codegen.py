# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

import abc

from typing import Dict

from vuepy import log
# due to a circular import
# from vuepy.compiler_sfc.codegen_backends.backend import INode

logger = log.getLogger()


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

    @abc.abstractmethod
    def _convert_slot_nodes_to_widgets(self, slots: Dict):
        pass

    @abc.abstractmethod
    def render(self, ctx, props, setup_returned) -> "INode":
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
        raise NotImplementedError
