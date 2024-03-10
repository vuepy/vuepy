from pathlib import Path

import anywidget
import traitlets
import ipywidgets as widgets


class ClipboardWidget(anywidget.AnyWidget):
    _esm = Path(__file__).parent / 'index.js'
    _css = Path(__file__).parent / 'index.css'

    tag = traitlets.Unicode('div').tag(sys=False)
    copy = traitlets.Unicode('').tag(sync=True)
    value = traitlets.Int(1).tag(sync=True)
    children = traitlets.List(trait=traitlets.Instance(widgets.DOMWidget)) \
        .tag(sync=True, **widgets.widget_serialization)
