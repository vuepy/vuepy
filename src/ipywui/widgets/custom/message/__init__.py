import time
from pathlib import Path

import anywidget
import traitlets


class Message(anywidget.AnyWidget):
    _instance = None
    _is_inited = False

    _esm = Path(__file__).parent / 'index.js'
    _css = Path(__file__).parent / 'index.css'

    message_options = traitlets.Dict().tag(sync=True)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not Message._is_inited:
            super().__init__(*args, **kwargs)
            Message._is_inited = True

    def _send_message(self, options):
        options['keep_change'] = time.time()
        self.message_options = options

    def success(self, options):
        options['type'] = 'success'
        self._send_message(options)

    def info(self, options):
        options['type'] = 'info'
        self._send_message(options)

    def warning(self, options):
        options['type'] = 'warning'
        self._send_message(options)

    def error(self, options):
        options['type'] = 'error'
        self._send_message(options)
