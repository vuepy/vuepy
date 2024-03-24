from ipywui.widgets.custom.message import MessageService
from vuepy import Vue
from vuepy import VueComponent
from vuepy import VuePlugin
from vuepy.utils.factory import FactoryMeta


class wui(VuePlugin, metaclass=FactoryMeta):
    @classmethod
    def install(cls, vm: Vue, options: dict):
        components = cls.get_all_registry()
        for name, component in components.items():
            vm.component(name, component)

        vm.message = MessageService(app_instance=vm)
        vm.document.body.appendLeftChild(vm.message.widget)


class IPywidgetsComponent(VueComponent):
    @classmethod
    def name(cls):
        # todo
        # return f'Ipw{cls.__name__}'
        return cls.__name__.lower()


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