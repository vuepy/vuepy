from typing import Any
from typing import Callable
from typing import List


# 应用实例

class Component:
    pass


class Element:
    pass


class Plugin:
    def __init__(self):
        pass

    def install(self, options):
        pass


class CompilerOptions:
    def __init__(self):
        self.whitespace = 'condense' # 'preserve'
        # 用于调整模板内文本插值的分隔符
        self.delimiters: List[str, str] = ['{{', '}}']
        # 用于调整是否移除模板中的 HTML 注释
        self.comments: bool = False

    def is_custom_element(self, tag: str) -> bool:
        """
        用于指定一个检查方法来识别原生自定义元素。

        :param tag:
        :return:
        """
        pass


class ComponentOptions:
    def __init__(self):
        self.compiler_options: CompilerOptions = CompilerOptions()
        self.setup = None

    # def data(self, this: "ComponentPublicInstance", vm: "ComponentPublicInstance") -> dict:
    #     """
    #     用于声明组件初始响应式状态的函数。
    #
    #     :param this:
    #     :param vm:
    #     :return:
    #     """
    #     pass


class Directive:
    pass


class ComponentPublicInstance:
    pass


class ErrorHandler:
    def __call__(self, err, instance: ComponentPublicInstance, info: str):
        """
        用于为应用内抛出的未捕获错误指定一个全局处理函数。

        :param err: 错误对象
        :param instance: 触发该错误的组件实例
        :param info: 指出错误来源类型信息，错误代码
        """
        pass


class WarningHandler:
    def __call__(self, msg: str, instance: ComponentPublicInstance, trace: str):
        """
        用于为 Vue 的运行时警告指定一个自定义处理函数。

        :param msg: 警告信息
        :param instance: 来源组件实例
        :param trace: 组件追踪字符串
        :return:
        """
        pass


class OptionMergeFunction:
    def __call__(self, to, from_):
        pass


class AppConfig:
    """应用的配置设定"""
    def __init__(self):
        self.error_handler: ErrorHandler = None
        self.warn_handler: WarningHandler = None
        self.performance: bool = False
        self.compiler_options: CompilerOptions = CompilerOptions()
        self.global_properties: dict[str, Any] = {}
        self.option_merge_strategies: dict[str, OptionMergeFunction] = {}


class App:
    """ 应用 """

    def __init__(self):
        self.config: AppConfig = AppConfig()

    def mount(self, root_container: Element | str) -> ComponentPublicInstance:
        """
        将应用实例挂载在一个容器元素中。

        app.mount('#app')
        app.mount(document.body.firstChild)

        :param root_container:
        :return:
        """
        pass

    def unmount(self) -> None:
        pass

    def component(self, name: str, component: Component = None) -> Component | "App":
        """
        如果同时传递一个组件名字符串及其定义，则注册一个全局组件；
        如果只传递一个名字，则会返回用该名字注册的组件 (如果存在的话)。

        query component(name) -> Component | None
        register component(name, component) -> self

        :param name:
        :param component:
        :return:
        """
        pass

    def directive(self, name: str, directive: Directive = None) -> Directive | "App":
        """
        如果同时传递一个名字和一个指令定义，则注册一个全局指令；
        如果只传递一个名字，则会返回用该名字注册的指令 (如果存在的话)。

        query directive(name) -> Directive | None
        register directive(name) -> self

        :param name:
        :param directive:
        :return:
        """
        pass

    def use(self, plugin: Plugin, *options) -> "App":
        """
        安装一个插件。
        若 app.use() 对同一个插件多次调用，该插件只会被安装一次。

        :param plugin: 插件本身
        :param options: 要传递给插件的选项
        :return:
        """
        pass

    def provide(self, key: str, value) -> "App":
        """
        提供一个值，可以在应用中的所有后代组件中注入使用。
        provide<T>(key: InjectionKey<T> | symbol | string, value: T): this
        app.provide('message', 'hello')

        :param key:
        :param value:
        :return:
        """
        pass

    def run_with_context(self, fn: Callable[[], str]):
        pass

    @property
    def version(self) -> str:
        """
        提供当前应用所使用的 Vue 版本号

        :return:
        """
        return ''


def create_app(root_component: Component, root_props: dict = None) -> App:
    """创建一个应用实例
    app = create_app(App)
    app = create_app({})

    :param root_component:
    :param root_props:
    :return:
    """
    pass


# 通用

version = '0.0.1'


def next_tick(callback: Callable):
    pass


class ComponentConstructor:
    pass


def define_component1(component: ComponentOptions) -> ComponentConstructor:
    """
    在定义 Vue 组件时提供类型推导的辅助函数。
    实际上在运行时没有任何操作，仅用于提供类型推导。

    :param component: 组件选项对象
    :return: 该选项对象本身
    """
    pass


class SetupContext:
    def __init__(self):
        self.attrs = {}
        self.slots = {}
        # 触发事件
        self.emit = {}
        # 暴露公共属性
        self.expose = {}


class h:
    pass


class Setup:
    def __call__(self, props: dict, context: SetupContext) -> dict | Callable[[], h]:
        """
        在将来，我们计划提供一个 Babel 插件，自动推断并注入运行时 props (就像在 SFC 中的 defineProps 一样)，以便省略运行时 props 的声明。
        使用场景：
        1. 需要在非单文件组件中使用组合式 API 时。
        2. 需要在基于选项式 API 的组件中集成基于组合式 API 的代码时

        :param props: 组件的 props，和标准的组件一致
        :param context: Setup上下文对象
        :return: 返回的对象会暴露给模板和组件实例
        """
        return locals()


def define_component(setup: Setup, extra_options: ComponentOptions) -> Callable[[], Any]:
    """
    旨在与组合式 API 和渲染函数或 JSX 一起使用。

    :param setup:
    :param extra_options:
    :return:
    """
    pass


# 组合式 API


