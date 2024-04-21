from typing import List
from typing import Tuple

from ipywui.widgets.custom.message import MessageService
from vuepy import App
from vuepy import VueComponent
from vuepy import VuePlugin
from vuepy.utils.factory import FactoryMeta


class wui(VuePlugin, metaclass=FactoryMeta):
    @classmethod
    def install(cls, app: App, options: dict):
        components = cls.get_all_registry()
        for name, component in components.items():
            app.component(name, component)

        app.message = MessageService(app_instance=app)
        app.document.body.appendLeftChild(app.message.widget)


class IPywidgetsComponent(VueComponent):
    STYLE_ATTR = 'style'
    CSS_TO_WIDGET_STYLE_MAP = {
        "background_color": "button_color",
        "color": "text_color",
    }
    LAYOUT_ATTRS = {
        # size
        "height",
        "width",
        "max_height",
        "max_width",
        "min_height",
        "min_width",
        # display
        "visibility",
        "display",
        "overflow",
        # box model
        "border",
        "margin",
        "padding",
        # positioning
        "top",
        "left",
        "bottom",
        "right",
        # Flexbox
        "order",
        "flex_flow",
        "align_items",
        "flex",
        "align_self",
        "align_content",
        "justify_content",
    }

    PARAMS_STORE_TRUE: List[Tuple[str, bool]] = []

    def convert_css_style(self, styles):
        for css_attr, widget_attr in self.CSS_TO_WIDGET_STYLE_MAP.items():
            val = styles.pop(css_attr, None)
            if val:
                styles[widget_attr] = val

        return styles

    def parse_style(self, style):
        attrs_str = (kv.strip().split(':') for kv in style.rstrip(';').split(';'))
        attrs = ((k.strip().replace('-', '_'), v.strip()) for k, v in attrs_str)
        styles = {}
        layout = {}
        for attr, val in attrs:
            if attr in self.LAYOUT_ATTRS:
                layout[attr] = val
            else:
                styles[attr] = val

        ret = {}
        if styles:
            ret[self.STYLE_ATTR] = self.convert_css_style(styles)
        if layout:
            ret['layout'] = layout
        return ret

    def update_style(self, kw):
        styles = kw.pop(self.STYLE_ATTR, None)
        if styles:
            kw.update(self.parse_style(styles))

    def _process_store_true_params(self, attrs, props):
        params = {}
        for key, default in self.PARAMS_STORE_TRUE:
            params[key] = has_and_pop(attrs, key) or has_and_pop(props, key) or default

        return params

    @classmethod
    def name(cls):
        # todo
        # return f'Ipw{cls.__name__}'
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


def is_float(n):
    return isinstance(n, float)


def is_int(n):
    return isinstance(n, int)


def is_str(s):
    return isinstance(s, str)


def is_tuple(t):
    return isinstance(t, (tuple, list))