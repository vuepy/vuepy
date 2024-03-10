#!coding: utf-8
import ipywidgets as widgets
from ipywui.core import IPywidgets
from ipywui.core import IPywidgetsComponent
from ipywui.core import has_and_pop
from ipywui.core import is_float
from ipywui.core import is_int
from ipywui.widgets import DisplayViewer
from ipywui.widgets import MarkdownViewerWidget


@IPywidgets.register()
class AppLayout(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        return widgets.AppLayout(**slots, **props, **attrs)


@IPywidgets.register()
class VBox(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        return widgets.VBox(children=slots.get('default', []), **props, **attrs)


@IPywidgets.register()
class Template(VBox):
    pass


@IPywidgets.register()
class Box(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        return widgets.VBox(children=slots.get('default', []), **props, **attrs)


@IPywidgets.register()
class HBox(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        return widgets.HBox(children=slots.get('default', []), **props, **attrs)


@IPywidgets.register()
class AccordionItem(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        title = attrs.pop('title', '-')
        widget = widgets.VBox(children=slots.get('default', []), **props, **attrs)
        widget.title = title
        return widget


@IPywidgets.register()
class Accordion(IPywidgetsComponent):
    v_model_default = 'selected_index'

    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        children = slots.get('default', [])
        titles = [child.title for child in children]
        return widgets.Accordion(children=children, titles=titles, **props, **attrs)


@IPywidgets.register()
class Button(IPywidgetsComponent):
    v_model_default = 'description'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Button(**props, **attrs)


@IPywidgets.register()
class Checkbox(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Checkbox(**props, **attrs)


@IPywidgets.register()
class ColorsInput(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.ColorsInput(**props, **attrs)


@IPywidgets.register()
class Combobox(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Combobox(**props, **attrs)


@IPywidgets.register()
class Controller(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Controller(**props, **attrs)


@IPywidgets.register()
class Col(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        span = attrs.pop('span', 24)
        offset = attrs.pop('offset', 0)
        widget = widgets.VBox(children=slots.get('default', []), **props, **attrs)
        widget.span = span
        widget.offset = offset
        return widget


@IPywidgets.register()
class ColorPicker(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        params = {
            'disable': has_and_pop(attrs, 'disable'),
            'concise': has_and_pop(attrs, 'concise'),
        }
        return widgets.ColorPicker(**props, **attrs, **params)


@IPywidgets.register()
class DatePicker(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        params = {
            "disable": has_and_pop(attrs, 'disable'),
        }
        return widgets.DatePicker(**props, **attrs, **params)


@IPywidgets.register()
class DatetimePicker(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        params = {
            "disable": has_and_pop(attrs, 'disable'),
        }
        # todo widgets.NaiveDatetimePicker
        return widgets.DatetimePicker(**props, **attrs, **params)


@IPywidgets.register()
class Display(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        obj = props.pop('obj', '-')
        widget = DisplayViewer(obj, **props, **attrs)
        return widget


@IPywidgets.register()
class Dropdown(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Dropdown(**props, **attrs)


@IPywidgets.register()
class FileUpload(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.FileUpload(**props, **attrs)


@IPywidgets.register()
class FloatsInput(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.FloatsInput(**props, **attrs)


@IPywidgets.register()
class HTMLMath(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.HTMLMath(**props, **attrs)


@IPywidgets.register()
class ColorsInput(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.ColorsInput(**props, **attrs)


@IPywidgets.register()
class Image(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Image(**props, **attrs)


@IPywidgets.register()
class InputNumber(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
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

        return cls(**props, **attrs)


@IPywidgets.register()
class Label(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Label(**props, **attrs)


@IPywidgets.register()
class MarkdownViewer(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return MarkdownViewerWidget(**props, **attrs)


@IPywidgets.register()
class Password(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Password(**props, **attrs)


@IPywidgets.register()
class Play(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Play(**props, **attrs)


@IPywidgets.register()
class Progress(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.FloatProgress(**props, **attrs)


@IPywidgets.register()
class RadioButtons(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.RadioButtons(**props, **attrs)


@IPywidgets.register()
class Row(IPywidgetsComponent):
    N_ROWS = 1
    N_COLS = 24

    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        cols = slots.get('default', [])

        justify_content = has_and_pop(attrs, 'justify')
        params = {}
        if justify_content:
            params['justify_content'] = justify_content

        align_items = has_and_pop(attrs, 'align')
        if align_items:
            params['align_items'] = align_items

        grid_gap = has_and_pop(attrs, 'gutter')
        if grid_gap:
            params['grid_gap'] = grid_gap

        widget = widgets.GridspecLayout(self.N_ROWS, self.N_COLS, **props, **attrs, **params)
        idx = 0
        for col in cols:
            idx += col.offset
            widget[0, (slice(idx, col.span))] = col
            idx += col.span
        return widget


@IPywidgets.register()
class Select(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        if has_and_pop(attrs, 'multiple'):
            cls = widgets.SelectMultiple
        else:
            cls = widgets.Select

        params = {
            "disable": has_and_pop(attrs, 'disable'),
        }
        return cls(**props, **attrs, **params)


@IPywidgets.register()
class SelectNumbers(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        data_type = props.pop('data_type', 'float')
        value = props.get(self.v_model_default, [])
        if data_type == 'float' or any(is_float(n) for n in value):
            cls = widgets.FloatsInput
        else:
            cls = widgets.IntsInput

        return cls(**props, **attrs)


@IPywidgets.register()
class SelectTags(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        params = {
            'allow_duplicates': has_and_pop(attrs, 'allow_duplicates'),
        }
        return widgets.TagsInput(**props, **attrs, **params)


@IPywidgets.register()
class SelectColors(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        params = {
            'allow_duplicates': has_and_pop(attrs, 'allow_duplicates'),
        }
        return widgets.ColorsInput(**props, **attrs, **params)


@IPywidgets.register()
class Slider(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        value = props.get(self.v_model_default)
        step = props.get('step')
        if has_and_pop(attrs, 'range'):
            if is_float(step):
                cls = widgets.FloatRangeSlider
            elif is_int(step):
                cls = widgets.IntRangeSlider
            else:
                cls = widgets.SelectionRangeSlider
        elif is_float(value) or is_float(step):
            cls = widgets.FloatSlider
        elif is_int(value) and is_int(step):
            cls = widgets.IntSlider
        else:
            cls = widgets.SelectionSlider

        param = {
            "continuous_update": has_and_pop(attrs, "continuous_update"),
            "orientation": 'vertical' if has_and_pop(attrs, 'vertical') else 'horizontal',
            "disable": has_and_pop(attrs, 'disable'),
        }
        return cls(**props, **attrs, **param)


@IPywidgets.register()
class Stack(IPywidgetsComponent):
    v_model_default = 'selected_index'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Stack(**props, **attrs)


@IPywidgets.register()
class TabPane(IPywidgetsComponent):
    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        title = attrs.pop('title', '-')
        widget = widgets.VBox(children=slots.get('default', []), **props, **attrs)
        widget.title = title
        return widget


@IPywidgets.register()
class Tabs(IPywidgetsComponent):
    v_model_default = 'selected_index'

    def render(self, ctx, props, setup_returned):
        slots = ctx.get('slots', {})
        attrs = ctx.get('attrs', {})
        children = slots.get('default', [])
        titles = [child.title for child in children]
        return widgets.Tab(children=children, titles=titles, **props, **attrs)


@IPywidgets.register()
class Text(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        params = {
            "continuous_update": has_and_pop(attrs, "continuous_update"),
        }
        return widgets.Text(**props, **attrs, **params)


@IPywidgets.register()
class Textarea(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        params = {
            "continuous_update": has_and_pop(attrs, "continuous_update"),
        }
        return widgets.Textarea(**props, **attrs, **params)


@IPywidgets.register()
class TimePicker(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        params = {
            "disable": has_and_pop(attrs, 'disable'),
        }
        return widgets.TimePicker(**props, **attrs, **params)


@IPywidgets.register()
class ToggleButton(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.ToggleButton(**props, **attrs)


@IPywidgets.register()
class ToggleButtons(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.ToggleButtons(**props, **attrs)


@IPywidgets.register()
class Valid(IPywidgetsComponent):
    v_model_default = 'value'

    def render(self, ctx, props, setup_returned):
        attrs = ctx.get('attrs', {})
        return widgets.Valid(**props, **attrs)


__all__ = [
    "Accordion",
    "AccordionItem",
    "AppLayout",
    "Box",
    "Button",
    "Checkbox",
    "Col",
    "ColorPicker",
    "ColorsInput",
    "ColorsInput",
    "Combobox",
    "Controller",
    "DatePicker",
    "DatetimePicker",
    "Display",
    "Dropdown",
    "FileUpload",
    "FloatsInput",
    "HBox",
    "HTMLMath",
    "Image",
    "InputNumber",
    "Label",
    "MarkdownViewer",
    "Password",
    "Play",
    "Progress",
    "RadioButtons",
    "Row",
    "Select",
    "SelectColors",
    "SelectNumbers",
    "SelectTags",
    "Slider",
    "Stack",
    "TabPane",
    "Tabs",
    "Template",
    "Text",
    "Textarea",
    "TimePicker",
    "ToggleButton",
    "ToggleButtons",
    "Valid",
    "VBox",
]
