from typing import List
from typing import Tuple

from vuepy import App
from vuepy import VueComponent
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


class IPyLeafletComponent(VueComponent):
    STYLE_ATTR = 'style'
    PARAMS_STORE_TRUE: List[Tuple[str, bool]] = []

    def update_style(self, kw):
        styles = kw.pop(self.STYLE_ATTR, None)
        # if styles:
            # kw.update(WidgetCssStyle.convert_css_style_to_widget_style_and_layout(styles))

    def _process_store_true_params(self, attrs, props):
        params = {}
        for key, default in self.PARAMS_STORE_TRUE:
            params[key] = has_and_pop(attrs, key) or has_and_pop(props, key) or default

        return params

    @classmethod
    def name(cls):
        return cls.__name__

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        params = self._process_store_true_params(attrs, props)

        self.update_style(attrs)
        self.update_style(props)

        return self._render(ctx, attrs, props, params, setup_returned)

    def _render(self, ctx, attrs, props, params, setup_returned):
        pass


def has_and_pop(attrs, key):
    if key in attrs:
        attrs.pop(key)
        return True
    return False 