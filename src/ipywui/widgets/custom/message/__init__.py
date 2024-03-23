import time
from pathlib import Path

import anywidget
import traitlets


class MessageItem:
    def __init__(self, message_widget, msg_id):
        self.message_widget = message_widget
        self.msg_id = msg_id

    def close(self):
        self.message_widget.close_msg(self.msg_id)


class MessageWidget(anywidget.AnyWidget):
    _esm = Path(__file__).parent / 'index.js'
    _css = Path(__file__).parent / 'index.css'

    message_options = traitlets.Dict({
        "message": '',
        "type": "info",
        "show_close": False,
        "duration": 3000,
    }).tag(sync=True)
    close_msg_id = traitlets.Unicode().tag(sync=True)

    def close_msg(self, msg_id):
        self.close_msg_id = msg_id

    def _send_message(self, options):
        msg_id = f"msg-{str(time.time())}"
        options['msg_id'] = msg_id
        self.message_options = options
        return MessageItem(self, msg_id)

    def success(self, options):
        options['type'] = 'success'
        return self._send_message(options)

    def info(self, options):
        options['type'] = 'info'
        return self._send_message(options)

    def warning(self, options):
        options['type'] = 'warning'
        return self._send_message(options)

    def error(self, options):
        options['type'] = 'error'
        return self._send_message(options)


class MessageService:
    _instance = {}
    _is_inited = {}

    def __new__(cls, *args, **kwargs):
        app = kwargs.get("app_instance")
        if app not in cls._instance:
            cls._instance[app] = super().__new__(cls)
        return cls._instance[app]

    def __init__(self, app_instance=None):
        if app_instance not in MessageService._is_inited:
            self.app = app_instance
            self.widget = MessageWidget()
            MessageService._is_inited[app_instance] = True

    def __call__(self, options=None, app_instance=None):
        message_service = MessageService(app_instance=app_instance)
        if options:
            return message_service.widget._send_message(options)
        return message_service

    def success(self, options):
        return self.widget.success(options)

    def info(self, options):
        return self.widget.info(options)

    def warning(self, options):
        return self.widget.warning(options)

    def error(self, options):
        return self.widget.error(options)


Message = MessageService()
