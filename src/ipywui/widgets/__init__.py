import pathlib
from typing import List

import ipywidgets as widgets
import markdown

from ipywui.widgets.custom.clipboard import ClipboardWidget
from ipywui.widgets.custom.dialog import DialogWidget
from ipywui.widgets.custom.message import Message
from vuepy.log import getLogger
from vuepy.utils.common import has_changed

logger = getLogger()


class WidgetNotSupported:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError(f"widget {self.__class__.__name__} not supported")


try:
    from ipywidgets import Password as _Password
except Exception as e:
    logger.warn("ipywidgets.Password import failed, fallback to Text.")
    _Password = widgets.Text

try:
    from ipywidgets import TimePicker as _TimePicker
except Exception as e:
    logger.warn(f"ipywidgets.TimePicker import failed, fallback to {WidgetNotSupported.__name__}.")

    class _TimePicker(WidgetNotSupported):
        pass

try:
    from ipywidgets import DatetimePicker as _DatetimePicker
except Exception as e:
    logger.warn(f"ipywidgets.DatetimePicker import failed, fallback to {WidgetNotSupported.__name__}.")

    class _DatetimePicker(WidgetNotSupported):
        pass

try:
    from ipywidgets import TagsInput as _TagsInput
except Exception as e:
    logger.warn(f"ipywidgets.TagsInput import failed, fallback to {WidgetNotSupported.__name__}.")

    class _TagsInput(WidgetNotSupported):
        pass

try:
    from ipywidgets import FloatsInput as _FloatsInput
except Exception as e:
    logger.warn(f"ipywidgets.FloatsInput import failed, fallback to {WidgetNotSupported.__name__}.")

    class _FloatsInput(WidgetNotSupported):
        pass

try:
    from ipywidgets import IntsInput as _IntsInput
except Exception as e:
    logger.warn(f"ipywidgets.IntsInput import failed, fallback to {WidgetNotSupported.__name__}.")

    class _IntsInput(WidgetNotSupported):
        pass

try:
    from ipywidgets import ColorsInput as _ColorsInput
except Exception as e:
    logger.warn(f"ipywidgets.ColorsInput import failed, fallback to {WidgetNotSupported.__name__}.")

    class _ColorsInput(WidgetNotSupported):
        pass


class WidgetCssStyle:
    WIDGET_STYLE_ATTR = 'style'
    WIDGET_LAYOUT_ATTR = 'layout'
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

    @classmethod
    def convert_css_style_to_widget_style_and_layout(cls, css_style: str) -> dict:
        """
        :param css_style:
        :return: {'style': {...}, 'layout': {...}}
        """
        attrs_str = (kv.strip().split(':') for kv in css_style.rstrip('; ').split(';'))
        attrs = ((k.strip().replace('-', '_'), v.strip()) for k, v in attrs_str)
        ret = {
            cls.WIDGET_STYLE_ATTR: {},
            cls.WIDGET_LAYOUT_ATTR: {},
        }
        for attr, val in attrs:
            if attr in cls.LAYOUT_ATTRS:
                ret[cls.WIDGET_LAYOUT_ATTR][attr] = val
            else:
                widget_style = cls.CSS_TO_WIDGET_STYLE_MAP.get(attr, attr)
                ret[cls.WIDGET_STYLE_ATTR][widget_style] = val

        return ret

    @property
    def css_style(self):
        return self.style

    @css_style.setter
    def css_style(self, value):
        if isinstance(value, str):
            value = self.convert_css_style_to_widget_style_and_layout(value)

        style = value.get(self.WIDGET_STYLE_ATTR)
        if style:
            self.style = style

        layout = value.get('layout')
        if layout:
            self.layout = layout


class AppLayout(widgets.AppLayout, WidgetCssStyle):
    pass


class VBox(widgets.VBox, WidgetCssStyle):
    pass


class HBox(widgets.HBox, WidgetCssStyle):
    pass


class Accordion(widgets.Accordion, WidgetCssStyle):
    pass


class MarkdownViewerWidget(widgets.HTML, WidgetCssStyle):
    code_highlight = pathlib.Path(__file__).parent / 'assets' / 'css' / 'md_code_highlight.css'
    with open(code_highlight) as f:
        css_style = ''.join(f.read())

    extra = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.tables',
        # 'markdown.extensions.nl2br',
    ]

    def __init__(self, value='', **kwargs):
        super().__init__(self.render(value), **kwargs)

    def render(self, md):
        html = markdown.markdown(md, extensions=self.extra)
        return f"<style>{self.css_style}</style>" + html

    def __setattr__(self, key, value):
        if key == 'value':
            value = self.render(value)

        super().__setattr__(key, value)


class BoundedFloatText(widgets.BoundedFloatText, WidgetCssStyle):
    pass


class BoundedIntText(widgets.BoundedIntText, WidgetCssStyle):
    pass


class Button(widgets.Button, WidgetCssStyle):
    CSS_TO_WIDGET_STYLE_MAP = {
        "background_color": "button_color",
        "color": "text_color",
    }

    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        kwargs['button_style'] = kwargs.pop("type", kwargs.pop('button_style', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val

    @property
    def type(self):
        return self.button_style

    @type.setter
    def type(self, val):
        self.button_style = val


class Checkbox(widgets.Checkbox, WidgetCssStyle):
    CSS_TO_WIDGET_STYLE_MAP = {}

    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class ColorPicker(widgets.ColorPicker, WidgetCssStyle):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class ColorsInput(_ColorsInput, WidgetCssStyle):
    def __init__(self, **kwargs):
        kwargs['allow_duplicates'] = not kwargs.pop("unique", not kwargs.pop('allow_duplicates', True))
        super().__init__(**kwargs)

    @property
    def unique(self):
        return not self.allow_duplicates

    @unique.setter
    def unique(self, val):
        self.allow_duplicates = not val


class Combobox(widgets.Combobox, WidgetCssStyle):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class Controller(widgets.Controller, WidgetCssStyle):
    pass


class DatePicker(widgets.DatePicker, WidgetCssStyle):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class DateTimePicker(_DatetimePicker, WidgetCssStyle):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class Dropdown(widgets.Dropdown, WidgetCssStyle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DisplayViewer(widgets.Output, WidgetCssStyle):
    def __init__(self, obj='', **kwargs):
        super().__init__(**kwargs)
        super().__setattr__('obj', obj)
        self.render(obj)

    def render(self, obj):
        self.clear_output()
        self.append_display_data(obj)

    def __setattr__(self, key, value):
        if key == 'obj' and has_changed(value, self.obj):
            self.render(value)

        super().__setattr__(key, value)


class FloatsInput(_FloatsInput, WidgetCssStyle):
    def __init__(self, **kwargs):
        kwargs['tag_style'] = kwargs.pop("type", kwargs.pop('tag_style', ''))
        super().__init__(**kwargs)


class FileUpload(widgets.FileUpload, WidgetCssStyle):
    pass


class FloatText(widgets.FloatText, WidgetCssStyle):
    pass


class FloatSlider(widgets.FloatSlider, WidgetCssStyle):
    pass


class FloatRangeSlider(widgets.FloatRangeSlider, WidgetCssStyle):
    pass


class FloatProgress(widgets.FloatProgress, WidgetCssStyle):
    CSS_TO_WIDGET_STYLE_MAP = {
        'color': 'bar_color',
    }

    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        kwargs['bar_style'] = kwargs.pop("type", kwargs.pop('bar_style', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val

    @property
    def type(self):
        return self.bar_style

    @type.setter
    def type(self, val):
        self.bar_style = val


class GridspecLayout(widgets.GridspecLayout, WidgetCssStyle):
    pass


class Label(widgets.Label, WidgetCssStyle):
    CSS_TO_WIDGET_STYLE_MAP = {
        'color': 'text_color',
    }


class HTMLMath(widgets.HTMLMath, WidgetCssStyle):
    pass


class Image(widgets.Image, WidgetCssStyle):
    pass


class IntText(widgets.IntText, WidgetCssStyle):
    pass


class IntSlider(widgets.IntSlider, WidgetCssStyle):
    pass


class IntRangeSlider(widgets.IntRangeSlider, WidgetCssStyle):
    pass


class IntsInput(_IntsInput, WidgetCssStyle):
    def __init__(self, **kwargs):
        kwargs['tag_style'] = kwargs.pop("type", kwargs.pop('tag_style', ''))
        super().__init__(**kwargs)


class Password(_Password, WidgetCssStyle):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class Play(widgets.Play, WidgetCssStyle):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class RadioButtons(widgets.RadioButtons, WidgetCssStyle):
    pass


class Select(widgets.Select, WidgetCssStyle):
    pass


class SelectMultiple(widgets.SelectMultiple, WidgetCssStyle):
    pass


class SelectionRangeSlider(widgets.SelectionRangeSlider, WidgetCssStyle):
    pass


class SelectionSlider(widgets.SelectionSlider, WidgetCssStyle):
    pass


class Stack(widgets.Stack, WidgetCssStyle):
    def __init__(self, **kwargs):
        self.labels: List[str] = kwargs.pop('labels', [])
        selected_label = kwargs.pop('label', self.labels[0])
        kwargs['selected_index'] = self.calc_selected_index_by_label(selected_label)
        super().__init__(**kwargs)

    @property
    def selected_label(self):
        return self.labels[self.selected_index or 0]

    @selected_label.setter
    def selected_label(self, label):
        try:
            self.selected_index = self.calc_selected_index_by_label(label)
        except Exception as e:
            logger.error(f"Set Stack selected_label({label}) failed, {e}")

    def calc_selected_index_by_label(self, label):
        return self.labels.index(label)


class Tab(widgets.Tab, WidgetCssStyle):
    pass


class TagsInput(_TagsInput, WidgetCssStyle):
    def __init__(self, **kwargs):
        kwargs['allow_duplicates'] = not kwargs.pop("unique", not kwargs.pop('allow_duplicates', True))
        super().__init__(**kwargs)

    @property
    def unique(self):
        return not self.allow_duplicates

    @unique.setter
    def unique(self, val):
        self.allow_duplicates = not val


class Text(widgets.Text, WidgetCssStyle):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class Textarea(widgets.Textarea, WidgetCssStyle):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class TimePicker(_TimePicker, WidgetCssStyle):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class ToggleButton(widgets.ToggleButton, WidgetCssStyle):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        kwargs['button_style'] = kwargs.pop("type", kwargs.pop('button_style', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val

    @property
    def type(self):
        return self.button_style

    @type.setter
    def type(self, val):
        self.button_style = val


class ToggleButtons(widgets.ToggleButtons, WidgetCssStyle):
    def __init__(self, **kwargs):
        kwargs['button_style'] = kwargs.pop("type", kwargs.pop('button_style', ''))
        super().__init__(**kwargs)

    @property
    def type(self):
        return self.button_style

    @type.setter
    def type(self, val):
        self.button_style = val


class Valid(widgets.Valid, WidgetCssStyle):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val
