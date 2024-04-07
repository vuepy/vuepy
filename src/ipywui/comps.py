#!coding: utf-8
import ipywidgets as widgets

import ipywui
from ipywui.core import IPywidgetsComponent
from ipywui.core import is_float
from ipywui.core import wui
from ipywui.widgets import ClipboardWidget
from ipywui.widgets import DialogWidget
from ipywui.widgets import DisplayViewer
from ipywui.widgets import MarkdownViewerWidget
from vuepy import log as logging

LOG = logging.getLogger()


@wui.register()
class AppLayout(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        return widgets.AppLayout(**slots, **props, **attrs)


@wui.register()
class VBox(IPywidgetsComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        return widgets.VBox(children=slots.get('default', []), **props, **attrs, **params)


@wui.register()
class Template(VBox):
    pass


@wui.register()
class Box(IPywidgetsComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        return widgets.VBox(children=slots.get('default', []), **props, **attrs, **params)


@wui.register()
class HBox(IPywidgetsComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        return widgets.HBox(children=slots.get('default', []), **props, **attrs, **params)


@wui.register()
class AccordionItem(IPywidgetsComponent):

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        title = attrs.pop('title', '-')
        widget = widgets.VBox(children=slots.get('default', []), **props, **attrs, **params)
        widget.title = title
        return widget


@wui.register()
class Accordion(IPywidgetsComponent):
    v_model_default = 'selected_index'

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        titles = [child.title for child in children]
        return widgets.Accordion(children=children, titles=titles, **props, **attrs, **params)


@wui.register()
class Button(IPywidgetsComponent):
    v_model_default = 'description'

    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipywui.widgets.Button(**props, **attrs, **params)


@wui.register()
class Checkbox(IPywidgetsComponent):
    v_model_default = 'value'

    CSS_TO_WIDGET_STYLE_MAP = {}

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        self.update_style(attrs)
        self.update_style(props)
        return ipywui.widgets.Checkbox(**props, **attrs)


@wui.register()
class ColorPicker(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('concise', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipywui.widgets.ColorPicker(**props, **attrs, **params)


@wui.register()
class Combobox(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipywui.widgets.Combobox(**props, **attrs, **params)


@wui.register()
class Controller(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Controller(**props, **attrs)


@wui.register()
class Clipboard(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        slots = ctx.get('slots', {})
        return ClipboardWidget(children=slots.get('default', []), **props, **attrs)


@wui.register()
class Col(IPywidgetsComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        widget = widgets.VBox(children=slots.get('default', []), **props, **attrs)

        widget.span = attrs.pop('span', 24)
        widget.offset = attrs.pop('offset', 0)
        return widget


@wui.register()
class DatePicker(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ("disabled", False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipywui.widgets.DatePicker(**props, **attrs, **params)


@wui.register()
class DateTimePicker(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ("disabled", False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        # todo widgets.NaiveDatetimePicker
        return ipywui.widgets.DateTimePicker(**props, **attrs, **params)


@wui.register()
class Dialog(IPywidgetsComponent):
    """
    仅支持放在最外层的VBOX中
    """
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        slot_body = slots.get('default', slots.get('body', []))
        slot_footer = slots.get('footer', [])
        attrs = ctx.get('attrs', {})
        widget = DialogWidget(body=slot_body, slot_footer=slot_footer, **props, **attrs)
        return widget


@wui.register()
class Display(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        obj = props.pop('obj', '-')
        widget = DisplayViewer(obj, **props, **attrs)
        return widget


@wui.register()
class Dropdown(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ("disabled", False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        return widgets.Dropdown(**props, **attrs, **params)


@wui.register()
class FileUpload(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ("multiple", False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        return widgets.FileUpload(**props, **attrs, **params)


@wui.register()
class FloatsInput(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.FloatsInput(**props, **attrs)


@wui.register()
class HTMLMath(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.HTMLMath(**props, **attrs)


@wui.register()
class Image(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Image(**props, **attrs)


@wui.register()
class Input(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ("disabled", False),
        ("continuous_update", False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _type = attrs.get('type', props.get('type', 'text'))
        if _type == 'password':
            cls = ipywui.widgets.Password
        elif _type == 'textarea':
            cls = ipywui.widgets.Textarea
        else:
            cls = ipywui.widgets.Text

        return cls(**props, **attrs, **params)


@wui.register()
class InputNumber(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ("disabled", False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        attrs = ctx.get('attrs', {})
        value = props.get(self.v_model_default)
        step = props.get('step')
        min_ = props.get('min')
        max_ = props.get('max')

        if is_float(value) or is_float(step):
            if is_float(min_) or is_float(max_):
                cls = widgets.BoundedFloatText
            else:
                cls = widgets.FloatText
        else:
            if min_ is None and max_ is None:
                cls = widgets.IntText
            else:
                cls = widgets.BoundedIntText

        return cls(**props, **attrs, **params)


@wui.register()
class Label(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Label(**props, **attrs)


@wui.register()
class MarkdownViewer(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return MarkdownViewerWidget(**props, **attrs)


@wui.register()
class Play(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipywui.widgets.Play(**props, **attrs, **params)


@wui.register()
class Progress(IPywidgetsComponent):
    v_model_default = 'value'

    CSS_TO_WIDGET_STYLE_MAP = {
        'color': 'bar_color',
    }

    PARAMS_STORE_TRUE = [
        ('vertical', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        params["orientation"] = 'vertical' if params.get("vertical") else 'horizontal'

        return ipywui.widgets.FloatProgress(**props, **attrs, **params)


@wui.register()
class RadioButtons(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        return widgets.RadioButtons(**props, **attrs, **params)


@wui.register()
class Row(IPywidgetsComponent):
    N_ROWS = 1
    N_COLS = 24

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        cols = slots.get('default', [])

        justify_content = attrs.pop('justify', props.pop('justify', None))
        if justify_content:
            params['justify_content'] = justify_content

        align_items = attrs.pop('align', props.pop('align', None))
        if align_items:
            params['align_items'] = align_items

        grid_gap = attrs.pop('gutter', props.pop('gutter', None))
        if grid_gap:
            params['grid_gap'] = grid_gap

        widget = widgets.GridspecLayout(self.N_ROWS, self.N_COLS, **props, **attrs, **params)
        idx = 0
        for col in cols:
            idx += col.offset
            widget[0, slice(idx, idx + col.span)] = col
            idx += col.span
        return widget


@wui.register()
class Select(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('multiple', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        multiple = params.pop('multiple', False)
        if multiple:
            cls = widgets.SelectMultiple
        else:
            cls = widgets.Select

        return cls(**props, **attrs, **params)


@wui.register()
class SelectColors(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ('unique', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipywui.widgets.ColorsInput(**props, **attrs, **params)


@wui.register()
class SelectNumbers(IPywidgetsComponent):
    v_model_default = 'value'

    def _render(self, ctx, attrs, props, params, setup_returned):
        attrs = ctx.get('attrs', {})
        data_type = attrs.pop('data_type', props.pop('data_type', 'float'))
        value = props.get(self.v_model_default, [])
        if data_type == 'float' or any(is_float(n) for n in value):
            cls = ipywui.widgets.FloatsInput
        else:
            cls = ipywui.widgets.IntsInput

        return cls(**props, **attrs)


@wui.register()
class SelectTags(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ('unique', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipywui.widgets.TagsInput(**props, **attrs, **params)


@wui.register()
class Slider(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ("disabled", False),
        ("continuous_update", False),
        ('vertical', False),
        ('range', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        params["orientation"] = 'vertical' if params.get("vertical") else 'horizontal'
        attrs = ctx.get('attrs', {})
        value = props.get(self.v_model_default)
        step = props.get('step')
        select_options = props.get('options', attrs.get('options', None))
        if params.pop('range', False):
            if select_options:
                cls = widgets.SelectionRangeSlider
            elif (value and is_float(value[0])) or is_float(step):
                cls = widgets.FloatRangeSlider
            else:
                cls = widgets.IntRangeSlider
        else:
            if select_options:
                cls = widgets.SelectionSlider
            elif is_float(value) or is_float(step):
                cls = widgets.FloatSlider
            else:
                cls = widgets.IntSlider

        return cls(**props, **attrs, **params)


@wui.register()
class Stack(IPywidgetsComponent):
    v_model_default = 'selected_index'

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        return widgets.Tab(children=children, **props, **attrs, **params)


@wui.register()
class TabPane(IPywidgetsComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        title = attrs.pop('title', '-')
        widget = widgets.VBox(children=slots.get('default', []), **props, **attrs, **params)
        widget.title = title
        return widget


@wui.register()
class Tabs(IPywidgetsComponent):
    v_model_default = 'selected_index'

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        titles = [child.title for child in children]
        return widgets.Tab(children=children, titles=titles, **props, **attrs, **params)


@wui.register()
class TimePicker(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ("disabled", False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipywui.widgets.TimePicker(**props, **attrs, **params)


@wui.register()
class ToggleButton(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipywui.widgets.ToggleButton(**props, **attrs, **params)


@wui.register()
class ToggleButtons(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipywui.widgets.ToggleButtons(**props, **attrs, **params)


@wui.register()
class Valid(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Valid(**props, **attrs)
