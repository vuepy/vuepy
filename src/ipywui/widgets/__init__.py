import pathlib
from typing import List

import ipywidgets as widgets
import markdown
from IPython.core.display_functions import clear_output
from IPython.core.display_functions import display

from ipywui.widgets.custom.clipboard import ClipboardWidget
from ipywui.widgets.custom.dialog import DialogWidget
from ipywui.widgets.custom.message import Message
from vuepy.log import getLogger

LOG = getLogger()


class MarkdownViewerWidget(widgets.HTML):
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


class Button(widgets.Button):
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


class Checkbox(widgets.Checkbox):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class ColorPicker(widgets.ColorPicker):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class ColorsInput(widgets.ColorsInput):
    def __init__(self, **kwargs):
        kwargs['allow_duplicates'] = not kwargs.pop("unique", not kwargs.pop('allow_duplicates', True))
        super().__init__(**kwargs)

    @property
    def unique(self):
        return not self.allow_duplicates

    @unique.setter
    def unique(self, val):
        self.allow_duplicates = not val


class Combobox(widgets.Combobox):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class DatePicker(widgets.DatePicker):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class DateTimePicker(widgets.DatetimePicker):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class Dropdown(widgets.Dropdown):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class DisplayViewer(widgets.Output):
    def __init__(self, obj='', **kwargs):
        super().__init__(**kwargs)
        self.render(obj)

    def render(self, obj):
        with self:
            clear_output()
            display(obj)

    def __setattr__(self, key, value):
        if key == 'obj':
            self.render(value)

        super().__setattr__(key, value)


class FloatsInput(widgets.FloatsInput):
    def __init__(self, **kwargs):
        kwargs['tag_style'] = kwargs.pop("type", kwargs.pop('tag_style', ''))
        super().__init__(**kwargs)


class FloatProgress(widgets.FloatProgress):
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
        return self.button_style

    @type.setter
    def type(self, val):
        self.button_style = val


class IntsInput(widgets.IntsInput):
    def __init__(self, **kwargs):
        kwargs['tag_style'] = kwargs.pop("type", kwargs.pop('tag_style', ''))
        super().__init__(**kwargs)


class Password(widgets.Password):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class Play(widgets.Play):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class Stack(widgets.Stack):
    def __init__(self, **kwargs):
        self.labels: List[str] = kwargs.pop('labels', [])
        super().__init__(**kwargs)

    @property
    def selected_label(self):
        return self.labels[self.selected_index]

    @selected_label.setter
    def selected_label(self, val):
        try:
            self.selected_index = self.labels.index(val)
        except Exception:
            pass


class TagsInput(widgets.TagsInput):
    def __init__(self, **kwargs):
        kwargs['allow_duplicates'] = not kwargs.pop("unique", not kwargs.pop('allow_duplicates', True))
        super().__init__(**kwargs)

    @property
    def unique(self):
        return not self.allow_duplicates

    @unique.setter
    def unique(self, val):
        self.allow_duplicates = not val


class Text(widgets.Text):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class Textarea(widgets.Textarea):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class TimePicker(widgets.TimePicker):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val


class ToggleButton(widgets.ToggleButton):
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


class ToggleButtons(widgets.ToggleButtons):
    def __init__(self, **kwargs):
        kwargs['button_style'] = kwargs.pop("type", kwargs.pop('button_style', ''))
        super().__init__(**kwargs)

    @property
    def type(self):
        return self.button_style

    @type.setter
    def type(self, val):
        self.button_style = val


class Valid(widgets.Valid):
    def __init__(self, **kwargs):
        kwargs['description'] = kwargs.pop("label", kwargs.pop('description', ''))
        super().__init__(**kwargs)

    @property
    def label(self):
        return self.description

    @label.setter
    def label(self, val):
        self.description = val
