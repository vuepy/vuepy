# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations
from types import MethodType

from textual.widgets.option_list import Option as OptionItem
from textual.widgets.selection_list import Selection as SelectionItem

from textual_vuepy.core import VTextualComponent, vtextual
from textual_vuepy import widgets


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
class VBox(VTextualComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        return widgets.VBox(*children, **_params)


@vtextual.ns_register()
class HBox(VTextualComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        return widgets.HBox(*children, **_params)


@vtextual.ns_register('slot')
class Slot(VBox):
    pass


@vtextual.ns_register()
class Button(VTextualComponent):
    v_model_default = 'label'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
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
    v_model_default = 'index'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        return widgets.ContentSwitcher(*children, **_params)


@vtextual.ns_register()
class DataTable(VTextualComponent):
    v_model_default = 'data'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        cols = _params.pop('cols', [])
        rows = _params.pop('rows', [])
        table = widgets.DataTable(**_params)

        def on_mount(self):
            self.add_columns(*cols)
            self.add_rows(rows)
            print('on_mount')

        # todo
        # setattr(table, 'on_mount', MethodType(on_mount, table))
        on_mount(table)

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
        return widgets.DirectoryTree(**_params)


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
    v_model_default = 'options'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        print(children)
        return widgets.OptionList(*children, **_params)


@vtextual.ns_register()
class Option(VTextualComponent):
    v_model_default = 'prompt'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return OptionItem(**_params)


@vtextual.ns_register()
class OptionGroup(VTextualComponent):
    v_model_default = 'label'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.OptionGroup(**_params)


@vtextual.ns_register()
class Placeholder(VTextualComponent):
    v_model_default = ''
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Placeholder(**_params)


@vtextual.ns_register()
class Pretty(VTextualComponent):
    v_model_default = 'data'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.Pretty(**_params)


@vtextual.ns_register()
class ProgressBar(VTextualComponent):
    v_model_default = 'progress'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.ProgressBar(**_params)


@vtextual.ns_register()
class RadioButton(VTextualComponent):
    v_model_default = 'selected'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return widgets.RadioButton(**_params)


@vtextual.ns_register()
class RadioSet(VTextualComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        return widgets.RadioSet(*children, **_params)


@vtextual.ns_register()
class RichLog(VTextualComponent):
    v_model_default = 'lines'
    PARAMS_STORE_TRUE = []

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
    v_model_default = 'tabs'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
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
    v_model_default = 'tabs'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        slots = ctx.get('slots', {})
        children = slots.get('default', [])
        return widgets.Tabs(*children, **_params)


@vtextual.ns_register()
class TextArea(VTextualComponent):
    v_model_default = 'text'
    PARAMS_STORE_TRUE = []

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
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
