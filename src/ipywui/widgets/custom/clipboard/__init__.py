from pathlib import Path

import anywidget
import traitlets
import ipywidgets as widgets

from vuepy.runtime.core.api_setup_helpers import defineEmits


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
        self.emits = defineEmits(['copy'])

    def on_copy(self, callback, remove=False):
        self.emits.add_event_listener('copy', callback, remove)

    def _on_event(self, change):
        event = change.get("new", {})
        ev = event.get("event")
        payload = event.get("payload")
        self.emits(ev, payload)
