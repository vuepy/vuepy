from pathlib import Path

import anywidget
import traitlets
import ipywidgets as widgets


class DialogWidget(anywidget.AnyWidget):
    _esm = Path(__file__).parent / 'index.js'
    _css = Path(__file__).parent / 'index.css'

    copy = traitlets.Unicode('').tag(sync=True)
    # Whether to display dialog
    value = traitlets.Bool(True).tag(sync=True)
    children = traitlets.List(trait=traitlets.Instance(widgets.DOMWidget)) \
        .tag(sync=True, **widgets.widget_serialization)
