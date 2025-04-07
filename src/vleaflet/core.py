from ipywui import IPywidgetsComponent
from vuepy import App
from vuepy.runtime.core.api_create_app import VuePlugin
from vuepy.utils.factory import FactoryMeta

_NAMESPACE = 'Vl'


class leaflet(VuePlugin, metaclass=FactoryMeta):
    @classmethod
    def install(cls, app: App, options: dict):
        components = cls.get_all_registry()
        for name, component in components.items():
            app.component(name, component)
    
    @classmethod
    def ns_register(cls, name=None):
        def _(sub_cls):
            _name = name or (sub_cls.name() if callable(sub_cls.name) else sub_cls.name)
            return cls.register(_NAMESPACE + _name)(sub_cls)
        return _


class IPyLeafletComponent(IPywidgetsComponent):
    pass
