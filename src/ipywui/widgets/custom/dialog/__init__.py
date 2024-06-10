from pathlib import Path

import anywidget
import traitlets
import ipywidgets as widgets

from vuepy.runtime.core.api_setup_helpers import defineEmits


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
        self.emits = defineEmits(['open', 'close'])

    def on_close(self, callback, remove=False):
        self.emits.add_event_listener('close', callback, remove)

    def on_open(self, callback, remove=False):
        self.emits.add_event_listener('open', callback, remove)

    def _on_event(self, change):
        event = change.get("new", {})
        payload = event.get("payload")
        ev = event.get("event")
        self.emits(ev, payload)

