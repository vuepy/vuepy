# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
"""
prompt: 参考 @comps.py @comps.py 为python panel库的 xxx 编写组件，保存到 @comps.py 中，一次性生成所有组件
"""
import panel as pn

from panel_vuepy.core import VPanelComponent, vpanel


@vpanel.ns_register()
class ChatAreaInput(VPanelComponent):
    """Panel ChatAreaInput component wrapper."""
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('auto_grow', True),
        ('disabled_enter', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        """Render the ChatAreaInput component."""
        _params = {**props, **attrs, **params}
        return pn.chat.ChatAreaInput(**_params)


@vpanel.ns_register()
class ChatFeed(VPanelComponent):
    """Panel ChatFeed component wrapper."""
    v_model_default = 'messages'
    PARAMS_STORE_TRUE = [
        ('show_timestamp', True),
        ('show_avatar', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        """Render the ChatFeed component."""
        _params = {**props, **attrs, **params}
        return pn.chat.ChatFeed(**_params)


@vpanel.ns_register()
class ChatInterface(VPanelComponent):
    """Panel ChatInterface component wrapper - a complete chat interface."""
    v_model_default = 'objects'
    PARAMS_STORE_TRUE = [
        ('show_rerun', True),
        ('show_undo', True),
        ('show_clear', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        """Render the ChatInterface component."""
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}
        widgets = slots.get('inputs')
        if widgets:
            _params['widgets'] = widgets.objects

        return pn.chat.ChatInterface(**_params)


@vpanel.ns_register()
class ChatMessage(VPanelComponent):
    """Panel ChatMessage component wrapper."""
    v_model_default = 'object'
    PARAMS_STORE_TRUE = [
        ('show_timestamp', True),
        ('show_avatar', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        """Render the ChatMessage component."""
        _params = {**props, **attrs, **params}
        return pn.chat.ChatMessage(**_params)


@vpanel.ns_register()
class ChatStep(VPanelComponent):
    """Panel ChatStep component wrapper for handling chat steps."""
    v_model_default = 'messages'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        """Render the ChatStep component."""
        _params = {**props, **attrs, **params}
        return pn.chat.ChatStep(**_params)


# @vpanel.ns_register()
# class PanelCallbackHandler(VPanelComponent):
#     """Panel CallbackHandler component wrapper for chat message callbacks."""
#     v_model_default = 'messages'
#     PARAMS_STORE_TRUE = [
#         ('stream', True),
#         ('reset_on_error', True),
#     ]

#     def _render(self, ctx, attrs, props, params, setup_returned):
#         """Render the PanelCallbackHandler component."""
#         _params = {**props, **attrs, **params}
#         return pn.chat.PanelCallbackHandler(**_params)
