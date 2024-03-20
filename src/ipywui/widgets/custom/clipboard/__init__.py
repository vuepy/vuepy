from pathlib import Path

import anywidget
import traitlets
import ipywidgets as widgets
from ipywidgets import CallbackDispatcher


class ClipboardWidget(anywidget.AnyWidget):
    _esm = Path(__file__).parent / 'index.js'
    _css = Path(__file__).parent / 'index.css'

    tag = traitlets.Unicode('div').tag(sys=False)
    copy = traitlets.Unicode('').tag(sync=True)
    event = traitlets.Dict().tag(sync=True)
    # slot
    children = traitlets.List(trait=traitlets.Instance(widgets.DOMWidget)) \
        .tag(sync=True, **widgets.widget_serialization)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.observe(self._on_event, ['event'])
        self._copy_handlers = CallbackDispatcher()

    def _on_event(self, change):
        event = change.get("new", {})
        ev = event.get("event")
        payload = event.get("payload")
        dispatch = {
            'copy': self._copy,
        }
        if ev in dispatch:
            dispatch[ev](payload)

    def on_copy(self, callback, remove=False):
        self._copy_handlers.register_callback(callback, remove=remove)

    def _copy(self, payload):
        self._copy_handlers(payload)
