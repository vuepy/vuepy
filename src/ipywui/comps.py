#!coding: utf-8
import ipywui
from ipywui.core import IPywidgetsComponent
from ipywui.core import is_float
from ipywui.core import wui
from ipywui.widgets import ClipboardWidget
from ipywui.widgets import DialogWidget
from ipywui.widgets import DisplayViewer
from ipywui.widgets import MarkdownViewerWidget
from vuepy import log as logging

logger = logging.getLogger()


@wui.register()
class AppLayout(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        return ipywui.widgets.AppLayout(**slots, **props, **attrs)


@wui.register()
class VBox(IPywidgetsComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        return ipywui.widgets.VBox(children=slots.get('default', []), **props, **attrs, **params)


@wui.register('template')
class Template(VBox):
    pass


@wui.register('slot')
class Slot(VBox):
    pass


@wui.register()
class Box(IPywidgetsComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        return ipywui.widgets.VBox(children=slots.get('default', []), **props, **attrs, **params)


@wui.register()
class HBox(IPywidgetsComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        return ipywui.widgets.HBox(children=slots.get('default', []), **props, **attrs, **params)


@wui.register()
class AccordionItem(IPywidgetsComponent):

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        title = attrs.pop('title', '-')
        widget = ipywui.widgets.VBox(children=slots.get('default', []), **props, **attrs, **params)
        widget.title = title
        return widget


@wui.register()
class Accordion(IPywidgetsComponent):
    v_model_default = 'selected_index'

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        titles = [child.title for child in children]
        return ipywui.widgets.Accordion(children=children, titles=titles, **props, **attrs, **params)


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
        return ipywui.widgets.Controller(**props, **attrs)


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
        widget = ipywui.widgets.VBox(children=slots.get('default', []), **props, **attrs)

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
        body = slot_body if isinstance(slot_body, list) else [slot_body]
        footer = slot_footer if isinstance(slot_footer, list) else [slot_footer]

        attrs = ctx.get('attrs', {})
        width = attrs.pop("layout", {}).pop("width", '50%')
        params = {
            'width': width,
        }
        widget = DialogWidget(body=body, footer=footer, **props, **attrs, **params)
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
        return ipywui.widgets.Dropdown(**props, **attrs, **params)


@wui.register()
class FileUpload(IPywidgetsComponent):
    v_model_default = 'value'

    PARAMS_STORE_TRUE = [
        ("multiple", False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipywui.widgets.FileUpload(**props, **attrs, **params)


@wui.register()
class HTMLMath(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return ipywui.widgets.HTMLMath(**props, **attrs)


@wui.register()
class Image(IPywidgetsComponent):
    v_model_default = 'value'

    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipywui.widgets.Image(**props, **attrs, **params)


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
                cls = ipywui.widgets.BoundedFloatText
            else:
                cls = ipywui.widgets.FloatText
        else:
            if min_ is None and max_ is None:
                cls = ipywui.widgets.IntText
            else:
                cls = ipywui.widgets.BoundedIntText

        return cls(**props, **attrs, **params)


@wui.register()
class Label(IPywidgetsComponent):
    v_model_default = 'value'

    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipywui.widgets.Label(**props, **attrs, **params)


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
        return ipywui.widgets.RadioButtons(**props, **attrs, **params)


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

        widget = ipywui.widgets.GridspecLayout(self.N_ROWS, self.N_COLS, **props, **attrs, **params)
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
            cls = ipywui.widgets.SelectMultiple
        else:
            cls = ipywui.widgets.Select

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
                cls = ipywui.widgets.SelectionRangeSlider
            elif (value and is_float(value[0])) or is_float(step):
                cls = ipywui.widgets.FloatRangeSlider
            else:
                cls = ipywui.widgets.IntRangeSlider
        else:
            if select_options:
                cls = ipywui.widgets.SelectionSlider
            elif is_float(value) or is_float(step):
                cls = ipywui.widgets.FloatSlider
            else:
                cls = ipywui.widgets.IntSlider

        return cls(**props, **attrs, **params)


@wui.register()
class Stack(IPywidgetsComponent):
    v_model_default = 'selected_label'

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        labels = [child.label for child in children]
        return ipywui.widgets.Stack(children=children, labels=labels, **props, **attrs, **params)


@wui.register()
class StackItem(IPywidgetsComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        label = props.pop('label', attrs.pop('label', '-'))
        widget = ipywui.widgets.VBox(children=slots.get('default', []), **props, **attrs, **params)
        widget.label = label
        return widget


@wui.register()
class TabPane(IPywidgetsComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        title = props.pop('title', attrs.pop('title', '-'))
        widget = ipywui.widgets.VBox(children=slots.get('default', []), **props, **attrs, **params)
        widget.title = title
        return widget


@wui.register()
class Tabs(IPywidgetsComponent):
    v_model_default = 'selected_index'

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        titles = [child.title for child in children]
        return ipywui.widgets.Tab(children=children, titles=titles, **props, **attrs, **params)


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

    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipywui.widgets.Valid(readout='', **props, **attrs, **params)
