# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

import abc
import dataclasses
from dataclasses import field
from typing import Any
from typing import Type
from typing import Union
import sys

from IPython.display import clear_output
from IPython.display import display

from vuepy import log
from vuepy.compiler_core.options import CompilerOptions
from vuepy.compiler_sfc import codegen_backends
from vuepy.compiler_sfc.codegen_backends import TEXTUAL_BACKEND, CodegenBackendMgr
from vuepy.compiler_sfc.codegen_backends.backend import ICodegenBackend
from vuepy.compiler_sfc.codegen_backends.backend import IDocumentNode
from vuepy.compiler_sfc.codegen_backends.backend import INode
from vuepy.compiler_sfc.sfc_codegen import SFC
from vuepy.compiler_sfc.sfc_codegen import SFCType
from vuepy.compiler_sfc.codegen import VueComponent
from vuepy.utils.common import Record

logger = log.getLogger()


@dataclasses.dataclass
class AppConfig:
    """应用的配置设定"""
    # error_handler: ErrorHandler
    # warn_handler: WarningHandler
    # option_merge_strategies: dict[str, OptionMergeFunction] = {}
    globalProperties: Record = field(default_factory=Record)
    compilerOptions: CompilerOptions = field(default_factory=CompilerOptions)
    performance: bool = False


class Directive:
    pass


@dataclasses.dataclass
class AppContext:
    app: 'App'
    config: AppConfig
    directives: dict[str, Directive]
    provides: dict[str, Any]
    components: dict[str, VueComponent] = field(default_factory=dict)


class App:
    components = {}

    def __init__(
        self, 
        root_component: RootComponent, 
        props: dict = None,
        backend: str | None = codegen_backends.ipywidgets.NAME, 
        servable: bool = False,
        debug: bool = False, 
    ):
        self.codegen_backend: ICodegenBackend = CodegenBackendMgr.get_by_name(backend)
        if self.codegen_backend is None:
            backends = CodegenBackendMgr.get_all_registry().keys()
            raise ValueError(f"backend should in {backends}, but '{backend}' found.")
        
        self.servable = servable
        if servable and not self.codegen_backend.is_servable():
            raise ValueError(f"backend {backend} is not servable.")

        self.config: AppConfig = AppConfig()

        self._installed_plugins = []
        self._props: dict = props or {}
        self._context: AppContext = AppContext(self, self.config, {}, {})
        self._instance: VueComponent = None

        if isinstance(root_component, dict):
            root_component = VueOptions(**root_component)

        # props = {}
        context = {}
        if isinstance(root_component, SFCType):
            self.root_component: SFC = root_component.gen(self._props, context, self)
        elif issubclass(root_component, VueComponent):
            self.root_component = root_component(self._props, context, self)
        else:
            raise ValueError(
                f"root_component only support {RootComponent}, {type(root_component)} found."
            )
        self.debug = debug

        self._components = {}
        self.component('template', self.codegen_backend.get_template_component())

        self.document: IDocumentNode = self.codegen_backend.gen_document_node(
            self.root_component
        )
        self.dom: INode = None

        self._proxy_methods()

    @property
    def version(self):
        import vuepy
        return vuepy.__version__

    def _call_if_callable(self, func):
        if callable(func):
            func(self)

    # def __getattr__(self, key):
    #     if key == '_data':
    #         return super().__getattribute__(key)
    #
    #     if key in self._data:
    #         return self._data[key]
    #
    #     return super().__getattribute__(key)
    #
    # def __setattr__(self, key, value):
    #     if key == '_data':
    #         return super().__setattr__(key, value)
    #
    #     if key in self._data:
    #         self._data[key] = value
    #         return
    #     return super().__setattr__(key, value)

    def _proxy_methods(self):
        pass

    def render(self):
        logger.info('App render start.')
        if not isinstance(self.root_component, VueComponent):
            raise ValueError(f"render failed, root_component type {type(self.root_component)}.")

        # self.dom = self.options.render({}, self._props, self._data)
        self.dom = self.root_component.render({}, {}, {})
        # with self.options.el:
        # with self._container:
        #     clear_output(True)
        #     display(self.dom)
        logger.info('App render end.')
        return self.dom

    def component(self, name: str, comp: Type['VueComponent'] = None) -> App:
        """
        query component(name) -> Component | None
        register component(name, comp) -> self

        :param name:
        :param comp:
        :return: self
        """
        # query
        if comp is None:
            return self._components.get(name, self.components.get(name, None))

        # register
        self._components[name] = comp
        return self

    def directive(self, name: str, directive: Directive = None) -> Directive | "App":
        """
        query directive(name) -> Directive | None
        register directive(name) -> self

        :param name:
        :param directive:
        :return:
        """
        pass

    def use(self, plugin: Type["VuePlugin"], options: dict = None) -> "App":
        """
        install plugin.

        :param plugin: 插件本身
        :param options: 要传递给插件的选项
        :return: self
        """
        if plugin in self._installed_plugins:
            return self

        plugin.install(self, options)
        return self

    def mount(self, *args, **kwargs):
        if self.codegen_backend.NAME == TEXTUAL_BACKEND:
            return self._mount_textual(*args, **kwargs)

        # self._call_if_callable(self.options.before_mount)
        self.render()
        # self._call_if_callable(self.options.mounted)

        # self.document.body_node.appendChild(self.dom)
        self.document.body.append(self.dom)

        widget = self.document.unwrap()
        if self.servable:
            widget.servable()
        return widget

    def _mount_textual(self, *args, **kwargs):
        run = kwargs.pop('run', True)
        def on_mount(tt_app):
            self.render()
            self.document.body.append(self.dom)

        self.tt_app = self.document.unwrap()
        self.tt_app.set_on_mount(on_mount)

        if not run:
            return self.tt_app

        self.tt_app.run(*args, **kwargs)

        if self.tt_app.message_:
            print(self.tt_app.message_)
        sys.exit(self.tt_app.return_code)


class VuePlugin:
    @classmethod
    @abc.abstractmethod
    def install(cls, app: App, options: dict):
        pass


VueOptions = SFCType

RootComponent = Union[Type[VueComponent], SFCType, dict]


def create_app(
    root_component: RootComponent, 
    use_wui: bool = True,
    backend: str = codegen_backends.ipywidgets.NAME,
    servable: bool = False,
    debug: bool = False,
    root_props: dict = None,
) -> App:
    """create a app instance.
    app = create_app(App)
    app = create_app({})

    :param root_component:
    :param use_wui: use ipywui
    :param backend: backend of codegen: ipywidgets, panel, etc. default: ipywidgets
    :param servable: servable mode
    :param debug: debug mode
    :param root_props: root component props
    :return:
    """
    app = App(
        root_component,
        backend=backend,
        debug=debug,
        servable=servable,
        props=root_props,
    )

    if backend == TEXTUAL_BACKEND:
        from textual_vuepy import vtextual
        app.use(vtextual)
    else:
        if use_wui:
            from ipywui import wui
            app.use(wui)

    return app
