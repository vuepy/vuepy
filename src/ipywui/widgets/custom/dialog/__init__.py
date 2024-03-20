from pathlib import Path

import anywidget
import traitlets
import ipywidgets as widgets
from ipywidgets import CallbackDispatcher


class DialogWidget(anywidget.AnyWidget):
    _esm = Path(__file__).parent / 'index.js'
    _css = Path(__file__).parent / 'index.css'

    title = traitlets.Unicode('').tag(sync=True)
    width = traitlets.Unicode('50%').tag(sync=True)
    # Whether to display dialog
    value = traitlets.Bool(False).tag(sync=True)
    event = traitlets.Dict().tag(sync=True)
    # slot
    body = traitlets.List(trait=traitlets.Instance(widgets.DOMWidget)) \
        .tag(sync=True, **widgets.widget_serialization)
    footer = traitlets.List(trait=traitlets.Instance(widgets.DOMWidget)) \
        .tag(sync=True, **widgets.widget_serialization)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.observe(self._on_event, ['event'])
        self._close_handlers = CallbackDispatcher()
        self._open_handlers = CallbackDispatcher()

    def on_close(self, callback, remove=False):
        self._close_handlers.register_callback(callback, remove=remove)

    def _close(self, payload):
        self._close_handlers(payload)

    def on_open(self, callback, remove=False):
        self._open_handlers.register_callback(callback, remove=remove)

    def _open(self, payload):
        self._open_handlers(payload)

    def _on_event(self, change):
        event = change.get("new", {})
        ev = event.get("event")
        payload = event.get("payload")
        dispatch = {
            'close': self._close,
            'open': self._open,
        }
        if ev in dispatch:
            dispatch[ev](payload)
