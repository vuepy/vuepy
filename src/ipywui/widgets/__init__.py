import pathlib

import ipywidgets as widgets
import markdown
from IPython.core.display_functions import clear_output
from IPython.core.display_functions import display

from ipywui.widgets.custom.clipboard import ClipboardWidget


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


__all__ = [
    "MarkdownViewerWidget",
    "DisplayViewer",
    "ClipboardWidget",
]