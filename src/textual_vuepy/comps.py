# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations
from types import MethodType
from pathlib import Path

from textual.widget import Widget
from textual.widgets.option_list import Option as OptionItem
from textual.widgets.selection_list import Selection as SelectionItem
from vuepy import import_sfc

from textual_vuepy.core import VTextualComponent, vtextual
from textual_vuepy import widgets

CURRENT_DIR = Path(__file__).parent
COMPONENTS_DIR = CURRENT_DIR / 'components'


@vtextual.ns_register()
class Dialog(VTextualComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        slot_body = slots.get('default', slots.get('body', []))
        slot_footer = slots.get('footer', [])
        body = slot_body if isinstance(slot_body, list) else [slot_body]
        footer = slot_footer if isinstance(slot_footer, list) else [slot_footer]
        _params.setdefault('name', f"dialog_{id(self)}")
        return widgets.Modal(body=body, footer=footer, **_params)


@vtextual.ns_register()
class Display(VTextualComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        obj: type[Widget] | Widget = _params.pop('obj')
        if isinstance(obj, type) and issubclass(obj, Widget):
            return obj(**_params)
        else:
            return obj


@vtextual.ns_register()
class VBox(VTextualComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        children = []
        # handle slots
        for _, child in slots.items():
            if isinstance(child, list):
                children.extend(child)
            else:
                children.append(child)
        return widgets.VBox(*children, **_params)


@vtextual.ns_register()
class HBox(VTextualComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        children = []
        # handle slots
        for _, child in slots.items():
            if isinstance(child, list):
                children.extend(child)
            else:
                children.append(child)
        return widgets.HBox(*children, **_params)


@vtextual.ns_register('slot')
class Slot(VBox):
    pass


@vtextual.ns_register()
class Button(VTextualComponent):
    v_model_default = 'label'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('flat', False),
    ]
    CONTENT_SLOT = ('default', 'label')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Button(**_params)


@vtextual.ns_register()
class Checkbox(VTextualComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Checkbox(**_params)


@vtextual.ns_register()
class Collapsible(VTextualComponent):
    v_model_default = 'collapsed'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        return widgets.Collapsible(*children, **_params)


@vtextual.ns_register()
class ContentSwitcher(VTextualComponent):
    # Textual: constructor `initial`, reactive attr `current` (str | None child id)
    # https://textual.textualize.io/widgets/content_switcher/
    v_model_default = 'current'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        # v-model / :current 传入的是 reactive 属性名，构造时需映射为 initial
        current = _params.pop(self.v_model_default, None)
        if current is not None and not _params.get('initial'):
            _params['initial'] = current
        return widgets.ContentSwitcher(*children, **_params)


@vtextual.ns_register()
class DataTable(VTextualComponent):
    v_model_default = 'data'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        cols = _params.pop('cols', None)
        rows = _params.pop('rows', None)
        table = widgets.DataTable(**_params)
        if cols is not None:
            table.cols = cols
        if rows is not None:
            table.rows = rows
        return table


@vtextual.ns_register()
class Digits(VTextualComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Digits(**_params)


@vtextual.ns_register()
class DirectoryTree(VTextualComponent):
    v_model_default = 'path'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.FilterableDirectoryTree(**_params)


@vtextual.ns_register()
class Footer(VTextualComponent):
    v_model_default = ''
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Footer(**_params)


@vtextual.ns_register()
class Header(VTextualComponent):
    v_model_default = ''
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        title = _params.pop('title', None)
        subtitle = _params.pop('subtitle', None)
        def _set_title(app):
            if title is not None:
                app.title = title
            if subtitle is not None:
                app.subtitle = subtitle
        _set_title(ctx['app'].tt_app)
        return widgets.Header(**_params)


@vtextual.ns_register()
class HelpPanel(VTextualComponent):
    v_model_default = ''
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.HelpPanel(**_params)


@vtextual.ns_register()
class Input(VTextualComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('compact', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Input(**_params)


@vtextual.ns_register()
class KeyPanel(VTextualComponent):
    v_model_default = ''
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.KeyPanel(**_params)


@vtextual.ns_register()
class Label(VTextualComponent):
    v_model_default = 'label'
    PARAMS_STORE_TRUE = []
    CONTENT_SLOT = ('default', 'label')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        label = _params.pop('label', None)
        return widgets.Label(label, **_params)


@vtextual.ns_register()
class Link(VTextualComponent):
    v_model_default = 'url'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Link(**_params)


@vtextual.ns_register()
class ListItem(VTextualComponent):
    v_model_default = 'label'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        return widgets.ListItem(*children, **_params)


@vtextual.ns_register()
class ListView(VTextualComponent):
    v_model_default = 'items'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        return widgets.ListView(*children, **_params)


@vtextual.ns_register()
class LoadingIndicator(VTextualComponent):
    v_model_default = 'show'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.LoadingIndicator(**_params)


@vtextual.ns_register()
class Log(VTextualComponent):
    v_model_default = 'lines'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Log(**_params)


@vtextual.ns_register()
class Markdown(VTextualComponent):
    v_model_default = 'markdown'
    PARAMS_STORE_TRUE = []
    CONTENT_SLOT = ('default', 'markdown')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Markdown(**_params)


@vtextual.ns_register()
class MarkdownViewer(VTextualComponent):
    v_model_default = 'markdown'
    PARAMS_STORE_TRUE = []
    CONTENT_SLOT = ('default', 'markdown')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.MarkdownViewer(**_params)


@vtextual.ns_register()
class MaskedInput(VTextualComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.MaskedInput(**_params)


@vtextual.ns_register()
class OptionList(VTextualComponent):
    v_model_default = 'selected'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        selected = _params.pop('selected', None)
        highlighted = _params.pop('highlighted', None)
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        opt_list = widgets.OptionList(*children, **_params)

        def set_initial(w):
            if highlighted is not None:
                w.highlighted = highlighted
            if selected is not None:
                w.selected = selected

        opt_list.vp_set_on_mount(set_initial)
        return opt_list


@vtextual.ns_register()
class Option(VTextualComponent):
    v_model_default = 'prompt'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return OptionItem(**_params)


@vtextual.ns_register()
class Placeholder(VTextualComponent):
    v_model_default = ''
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Placeholder(**_params)


@vtextual.ns_register()
class Pretty(VTextualComponent):
    # Textual: constructor positional `object`; update via Pretty.update()
    # https://textual.textualize.io/widgets/pretty/
    v_model_default = 'object'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        # 兼容文档里曾用的 data 别名
        obj = _params.pop('object', None)
        if obj is None and 'data' in _params:
            obj = _params.pop('data')
        return widgets.Pretty(obj, **_params)


@vtextual.ns_register()
class ProgressBar(VTextualComponent):
    v_model_default = 'progress'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        progress = _params.pop('progress', None)
        _w = widgets.ProgressBar(**_params)
        if progress is not None:
            _params['value'] = progress
            _w.progress = progress
        return _w


@vtextual.ns_register()
class RadioButton(VTextualComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        button_inner = _params.pop('button_inner', None)
        widget = widgets.RadioButton(**_params)
        if button_inner is not None:
            widget.BUTTON_INNER = button_inner
        return widget


@vtextual.ns_register()
class RadioSet(VTextualComponent):
    v_model_default = 'selected_index'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        # Textual RadioSet.__init__ 不接受 value，v-model 的 value 由 widget 创建后 setattr 设置
        vp_selected_index = _params.pop(self.v_model_default, None)
        # vp_selected_index = _params.pop('_selected', None)
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        return widgets.RadioSet(vp_selected_index, *children, **_params)


@vtextual.ns_register()
class RichLog(VTextualComponent):
    v_model_default = 'lines'
    PARAMS_STORE_TRUE = [
        ('markup', False),
        ('wrap', False),
        ('highlight', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.RichLog(**_params)


@vtextual.ns_register()
class Rule(VTextualComponent):
    v_model_default = ''
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Rule(**_params)


@vtextual.ns_register()
class Select(VTextualComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Select(**_params)


@vtextual.ns_register()
class SelectionList(VTextualComponent):
    v_model_default = 'selected'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        return widgets.SelectionList(*children, **_params)


@vtextual.ns_register()
class Selection(VTextualComponent):
    v_model_default = 'prompt'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return SelectionItem(**_params)


@vtextual.ns_register()
class Sparkline(VTextualComponent):
    v_model_default = 'data'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Sparkline(**_params)


@vtextual.ns_register()
class Static(VTextualComponent):
    v_model_default = 'content'
    PARAMS_STORE_TRUE = []
    CONTENT_SLOT = ('default', 'content')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Static(**_params)


@vtextual.ns_register()
class Switch(VTextualComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Switch(**_params)


@vtextual.ns_register()
class TabbedContent(VTextualComponent):
    # Textual: constructor `initial`, reactive attr `active` (tab pane id)
    # https://textual.textualize.io/widgets/tabbed_content/
    v_model_default = 'active'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        # v-model / :active → 构造参数 initial
        active = _params.pop('active', None)
        if active is not None and not _params.get('initial'):
            _params['initial'] = active
        tabbed_content = widgets.TabbedContent(**_params)
        for child in children:
            tabbed_content.compose_add_child(child)
        return tabbed_content


@vtextual.ns_register()
class TabPane(VTextualComponent):
    v_model_default = 'label'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        title = _params.pop('title')
        return widgets.TabPane(title, *children, **_params)


@vtextual.ns_register()
class Tab(VTextualComponent):
    v_model_default = 'label'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Tab(**_params)


@vtextual.ns_register()
class Tabs(VTextualComponent):
    # Textual: constructor + reactive attr `active` (tab id)
    # https://textual.textualize.io/widgets/tabs/
    v_model_default = 'active'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        return widgets.Tabs(*children, **_params)


@vtextual.ns_register()
class TextArea(VTextualComponent):
    v_model_default = 'text'
    PARAMS_STORE_TRUE = [
        ('code_editor', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        code_editor = _params.pop('code_editor', False)
        if code_editor:
            return widgets.TextArea.code_editor(**_params)
        else:
            return widgets.TextArea(**_params)


@vtextual.ns_register()
class Tooltip(VTextualComponent):
    v_model_default = 'text'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Tooltip(**_params)


@vtextual.ns_register()
class Tree(VTextualComponent):
    v_model_default = 'data'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Tree(**_params)


@vtextual.ns_register()
class Welcome(VTextualComponent):
    v_model_default = ''
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Welcome(**_params)


ShimmerText = import_sfc(COMPONENTS_DIR / 'ShimmerText.vue')
Spinner = import_sfc(COMPONENTS_DIR / 'Spinner.vue')
vtextual.ns_register('ShimmerText')(ShimmerText)
vtextual.ns_register('Spinner')(Spinner)
