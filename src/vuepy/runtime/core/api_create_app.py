from __future__ import annotations

import abc
import dataclasses
from dataclasses import field
from typing import Any
from typing import Type
from typing import Union

import ipywidgets as widgets
from IPython.core.display_functions import clear_output
from IPython.core.display_functions import display

from vuepy import log
from vuepy.compiler_core.options import CompilerOptions
from vuepy.compiler_sfc.codegen import Dom
from vuepy.compiler_sfc.codegen import SFC
from vuepy.compiler_sfc.codegen import SFCFactory
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
    compilerOptions: CompilerOptions = CompilerOptions()
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

    def __init__(self, root_component: RootComponent, debug=False):
        self.config: AppConfig = AppConfig()

        self._installed_plugins = []
        self._props: dict = {}
        self._container = None
        self._context: AppContext = AppContext(self, self.config, {}, {})
        self._instance: VueComponent = None

        if isinstance(root_component, dict):
            root_component = VueOptions(**root_component)

        props = {}
        context = {}
        if isinstance(root_component, SFCFactory):
            self.root_component: SFC = root_component.gen(props, context, self)
        else:
            raise ValueError(
                f"root_component only support {RootComponent}, {type(root_component)} found."
            )
        self.debug = debug

        self._components = {}

        self.document: Document = Document()
        self.dom = None

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
        if not isinstance(self.root_component, SFC):
            raise ValueError(f"render failed, root_component type {type(self.root_component)}.")

        # self.dom = self.options.render({}, self._props, self._data)
        self.dom = self.root_component.render()
        # with self.options.el:
        with self._container:
            clear_output(True)
            display(self.dom)
        logger.info('App render end.')

    def component(self, name: str, comp: 'VueComponent' = None) -> App:
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

    def mount(self, el=None):
        self._container = el or widgets.Output()
        # self._call_if_callable(self.options.before_mount)
        self.render()
        # self._call_if_callable(self.options.mounted)
        self.document.body.appendChild(self._container)
        return self.document


class VuePlugin:
    @classmethod
    @abc.abstractmethod
    def install(cls, app: App, options: dict):
        pass


VueOptions = SFCFactory

RootComponent = Type[Union[Type[VueComponent], SFCFactory, dict]]


def create_app(root_component: RootComponent, use_wui=True, **root_props) -> App:
    """创建一个应用实例
    app = create_app(App)
    app = create_app({})

    :param use_wui:
    :param root_component:
    :param root_props:
    :return:
    """
    debug = root_props.get('debug', False)
    app = App(root_component, debug)
    if use_wui:
        from ipywui import wui
        app.use(wui)
    return app


class Document(widgets.VBox):
    """
    https://developer.mozilla.org/en-US/docs/Web/API/Document
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body = Dom()
        self.children = (self.body,)
