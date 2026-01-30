# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

from types import MethodType
from typing import Callable

from textual import widgets
from textual.containers import HorizontalScroll, VerticalScroll
from textual.containers import Vertical
from textual.reactive import reactive
from textual.screen import ModalScreen

from vuepy import log
from vuepy.runtime.core.api_setup_helpers import defineEmits

logger = log.getLogger(__name__)

class _WidgetMixin:
    style: reactive[str] = reactive("", init=False)

    def __init__(self) -> None:
        self._on_keyup_cb = {}
        self._vp_on_mount_cb = []
    
    def vp_set_on_mount(self, cb: Callable[["Self"], None]):
        if not hasattr(self, '_vp_on_mount_cb'):
            self._vp_on_mount_cb = []
        self._vp_on_mount_cb.append(cb)
    
    def on_mount(self):
        if not hasattr(self, '_vp_on_mount_cb'):
            return

        for cb in self._vp_on_mount_cb:
            cb(self)

    def _watch_style(self) -> None:
        self.set_styles(self.style)

    def observe(self, attr: str, cb, remove=False):
        # watch 通过检测wrap函数的参数个数来决定传入几个参数，直接传cb无法检测，默认传2个参数，导致报错
        def cb_with_one_param(v):
            cb(v)

        self.app.watch(self, attr, cb_with_one_param)

    def action_keyup(self, key, *args):
        cb = self._on_keyup_cb[key]
        cb(*args)

    def register_on_keyup(self, key, cb):
        if not hasattr(self, '_on_keyup_cb'):
            self._on_keyup_cb = {}
        self._on_keyup_cb[key] = cb
        self.bind(key, f"keyup('{key}')", description=cb.__doc__, key_display=cb.__name__)

    def bind(
        self,
        keys: str,
        action: str,
        *,
        description: str = "",
        show: bool = True,
        key_display: str | None = None,
    ) -> None:
        """Bind a key to an action.

        !!! warning
            This method may be private or removed in a future version of Textual.
            See [dynamic actions](/guide/actions#dynamic-actions) for a more flexible alternative to updating bindings.

        Args:
            keys: A comma separated list of keys, i.e.
            action: Action to bind to.
            description: Short description of action.
            show: Show key in UI.
            key_display: Replacement text for key, or None to use default.
        """
        self._bindings.bind(
            keys, action, description, show=show, key_display=key_display
        )

    # def on_mouse_move(self, event: events.MouseMove) -> None:
    #     if not hasattr(self, '_on_mouse_move_cb'):
    #         return
    #     self._on_mouse_move_cb(event)

    # def register_on_mouse_move(self, cb):
    #     if not hasattr(self, '_on_mouse_move_cb'):
    #         self._on_mouse_move_cb = {}
    #     self._on_mouse_move_cb = cb

    def vp_register_on(self, event: str, cb):
        # todo add event check
        on_event_func_name = f"on_{event}"
        event_handler_func_name = f"_vp_{event}_handler"

        def on_event_func(this, event):
            if hasattr(this, event_handler_func_name):
                return getattr(this, event_handler_func_name)(event)

        if not hasattr(self, on_event_func_name):
            setattr(self.__class__, on_event_func_name, on_event_func)

        def event_handler(this, event):
            return cb(event)

        setattr(self, event_handler_func_name, MethodType(event_handler, self))

    # def register_on(self, event: str, cb):
    #     # todo check event [mouse_move, mouse_up]
    #     @wraps(cb)
    #     def on_xxx(this, *args, **kwargs):
    #         cb(*args, **kwargs)

    #     setattr(self, f"on_{event}", MethodType(on_xxx, self))


class Modal(ModalScreen, _WidgetMixin):
    DEFAULT_CSS = '''
        Modal {
            align: center middle;
        }

        #dialog {
            grid-size: 2;
            grid-gutter: 1 2;
            grid-rows: 1fr 3;
            padding: 0 1;
            width: 60;
            height: 11;
            border: thick $background 80%;
            background: $surface;
        }
    '''

    value: reactive[bool] = reactive(False, init=False)

    def __init__(self, *args, **kwargs):
        # self.__is_open = kwargs.pop('is_open', False)
        self.__body = kwargs.pop('body', [])
        self.__footer = kwargs.pop('footer', [])
        # self.__style = kwargs.pop('style', "")

        value = kwargs.pop('value', False)
        super().__init__(*args, **kwargs)
        self.value = value
        self.emits = defineEmits(['open', 'close'])

    def _watch_style(self):
        if not hasattr(self, 'dialog'):
            return
        self.dialog.set_styles(self.style)

    # @property
    # def style(self):
    #     return self.__style

    # @style.setter
    # def style(self, value):
    #     self.__style = value
    #     self.dialog.set_styles(value)

    def compose(self):
        self.dialog = Vertical(
            *self.__body,
            *self.__footer,
            id='dialog',
        )
        self.dialog.set_styles(self.style)
        # self.style = self.__style

        yield self.dialog

    def attach(self):
        """
        template_compiler::handle_endtag will call attach method to install 
        ModalScreen to app, not add to parent node.
        """
        name = self._name
        self.app._modes[name] = name
        self.app.uninstall_screen(name)
        self.app.install_screen(self, name=name)
        if self.value:
            self.open()

    def open(self):
        self.value = True

    def close(self):
        self.value = False

    def _watch_value(self) -> None:
        if self.value:
            self.app.push_screen(self)
            event = 'open'
        else:
            self.app.pop_screen()
            event = 'close'
        self.emits(event, '')

    def register_on_close(self, callback, remove=False):
        self.emits.add_event_listener('close', callback, remove)

    def register_on_open(self, callback, remove=False):
        self.emits.add_event_listener('open', callback, remove)


class Button(widgets.Button, _WidgetMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._vp_cb = {}

    def register_on_click(self, cb: callable, remove=False):
        self._vp_cb['click'] = cb

    def on_button_pressed(self, event: widgets.Button.Pressed) -> None:
        cb = self._vp_cb.get('click')
        if cb:
            cb(event)


class Checkbox(widgets.Checkbox, _WidgetMixin):
    pass


class Collapsible(widgets.Collapsible, _WidgetMixin):
    pass


class ContentSwitcher(widgets.ContentSwitcher, _WidgetMixin):
    pass


class DataTable(widgets.DataTable, _WidgetMixin):
    pass


class Digits(widgets.Digits, _WidgetMixin):
    pass


class DirectoryTree(widgets.DirectoryTree, _WidgetMixin):
    pass


class Footer(widgets.Footer, _WidgetMixin):
    pass


class Header(widgets.Header, _WidgetMixin):
    pass


class HelpPanel(widgets.HelpPanel, _WidgetMixin):
    pass


class Input(widgets.Input, _WidgetMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cb = {}

    # # v-model for reactive attr
    # def observe(self, attr: str, cb, remove=False):
    #     def wrap(v):
    #         cb(v)
    #
    #     self.app.watch(self, attr, wrap)


class VBox(VerticalScroll, _WidgetMixin):
    DEFAULT_CSS = '''
        VBox {
            height: auto;
            overflow-x: auto;
            overflow-y: auto;
        }
    '''

class HBox(HorizontalScroll, _WidgetMixin):
    DEFAULT_CSS = '''
        HBox {
            height: auto;
            overflow-x: auto;
            overflow-y: auto;
        }
    '''


class KeyPanel(widgets.KeyPanel, _WidgetMixin):
    pass


class Label(widgets.Label, _WidgetMixin):
    @property
    def label(self):
        return self._content

    @label.setter
    def label(self, value):
        self.update(value)


class Link(widgets.Link, _WidgetMixin):
    pass


class ListItem(widgets.ListItem, _WidgetMixin):
    pass


class ListView(widgets.ListView, _WidgetMixin):
    pass


class LoadingIndicator(widgets.LoadingIndicator, _WidgetMixin):
    pass


class Log(widgets.Log, _WidgetMixin):
    pass


class Markdown(widgets.Markdown, _WidgetMixin):
    @property
    def markdown(self):
        return self.source

    @markdown.setter
    def markdown(self, value):
        self.update(value)


class MarkdownViewer(widgets.MarkdownViewer, _WidgetMixin):
    @property
    def markdown(self):
        return self.document.source

    @markdown.setter
    def markdown(self, value):
        self.document.update(value)

class MaskedInput(widgets.MaskedInput, _WidgetMixin):
    pass


class OptionList(widgets.OptionList, _WidgetMixin):
    pass


class Placeholder(widgets.Placeholder, _WidgetMixin):
    pass


class Pretty(widgets.Pretty, _WidgetMixin):
    pass


class ProgressBar(widgets.ProgressBar, _WidgetMixin):
    pass


class RadioButton(widgets.RadioButton, _WidgetMixin):
    pass


class RadioSet(widgets.RadioSet, _WidgetMixin):
    def __init__(self, vp_selected_index: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        def _init_selected_index(self):
            self.selected_index = vp_selected_index

        self.vp_set_on_mount(_init_selected_index)
    
    @property
    def selected_index(self) -> int:
        return self.pressed_index

    @selected_index.setter
    def selected_index(self, index: int) -> None:
        buttons = list(self.query(widgets.RadioButton))
        # if not (0 <= index < len(buttons)):
        #     msg = f"Invalid index {index} for RadioSet {self}"
        #     logger.warning(msg)
        #     raise ValueError(msg)

        # 1. set radio set selected index
        self._selected = index
        # 2.set radio button value
        for i, btn in enumerate(buttons):
            btn.value = i == index
    
    def observe(self, attr: str, cb, remove=False):
        if attr == 'selected_index':
            def on_vp_selected_index_changed(event):
                cb(event.radio_set.selected_index)
            self.vp_register_on('radio_set_changed', on_vp_selected_index_changed)
        else:
            super().observe(attr, cb, remove)


class RichLog(widgets.RichLog, _WidgetMixin):
    pass


class Rule(widgets.Rule, _WidgetMixin):
    pass


class Select(widgets.Select, _WidgetMixin):
    pass


class SelectionList(widgets.SelectionList, _WidgetMixin):
    pass


class Sparkline(widgets.Sparkline, _WidgetMixin):
    pass


class Static(widgets.Static, _WidgetMixin):
    # @property
    # def value(self):
    #     return self._content

    # @value.setter
    # def value(self, value):
    #     self.update(value)
    pass


class Switch(widgets.Switch, _WidgetMixin):
    pass


class Tab(widgets.Tab, _WidgetMixin):
    pass


class TabbedContent(widgets.TabbedContent, _WidgetMixin):
    pass


class TabPane(widgets.TabPane, _WidgetMixin):
    pass


class Tabs(widgets.Tabs, _WidgetMixin):
    pass


class TextArea(widgets.TextArea, _WidgetMixin):
    # v-model for no reactive attr
    def observe(self, attr: str, cb, remove=False):
        if attr == 'text':
            def on_text_area_changed(event):
                cb(event.text_area.text)
            self.vp_register_on('text_area_changed', on_text_area_changed)
        else:
            super().observe(attr, cb, remove)


class Tooltip(widgets.Tooltip, _WidgetMixin):
    pass


class Tree(widgets.Tree, _WidgetMixin):
    pass


class Welcome(widgets.Welcome, _WidgetMixin):
    pass
