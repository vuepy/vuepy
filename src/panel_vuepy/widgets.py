# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations
from typing import Dict

import panel as pn
try:
    from panel.widgets import ButtonIcon as _ButtonIcon
except ImportError:
    _ButtonIcon = None
try:
    from panel.widgets import ToggleIcon as _ToggleIcon
except ImportError:
    _ToggleIcon = None

from vuepy.compiler_sfc.codegen_backends.backend import IHTMLNode
from vuepy.compiler_sfc.codegen_backends.backend import INode
from panel_vuepy.core import VPanelComponent, vpanel


@vpanel.ns_register()
class ArrayInput(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        m = pn.widgets.ArrayInput(**_params)
        return m


class ButtonComponent(VPanelComponent):
    _cls = pn.widgets.Button

    v_model_default = 'name'
    PARAMS_STORE_TRUE = [
        ('loading', False),
        ('disabled', False),
    ]

    def _convert_slot_nodes_to_widgets(self, slots: Dict | None):
        pass

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})

        # <slot name='default'>
        slot_labels = slots.get('default', [])
        slot_label_node: IHTMLNode = slot_labels[0] if slot_labels else None
        if slot_label_node:
            attrs[self.v_model_default] = slot_label_node.outer_html

        # <slot name='icon'>
        icon_slot: INode = slots.get('icon')
        if icon_slot:
            attrs['icon'] = icon_slot.inner_html

        _params = {**props, **attrs, **params}
        w = self._cls(**_params)

        # handle <slot name='default'> content change
        if slot_label_node:
            def _update_button_name(change):
                val = change['new'] if isinstance(change, dict) else change
                w.name = val

            slot_label_node.on_change(_update_button_name)

        return w


@vpanel.ns_register()
class Button(ButtonComponent):
    _cls = pn.widgets.Button


@vpanel.ns_register()
class AutocompleteInput(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('case_sensitive', False),
        ('restrict', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.AutocompleteInput(**_params)


class ActiveIconComponent(VPanelComponent):
    _cls = _ButtonIcon
    v_model_default = 'name'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]
    # tuple of (slot_name, widget_attr_name, slot_node_attr_name)
    SLOTS = [
        ('default', 'name' 'outer_name'),
        ('icon', 'icon' 'inner_html'),
        ('active-icon', 'active_icon' 'inner_html'),
    ]

    def _convert_slot_nodes_to_widgets(self, slots: Dict | None):
        pass

    def _process_slots(self, slots: Dict | None) -> Dict:
        if slots is None:
            return {}

        slot_attrs = {}
        for slot_name, widget_attr_name, slot_node_attr_name in self.SLOTS:
            slot_node = slots.get(slot_name)
            if not slot_node:
                continue
            slot_attrs[widget_attr_name] = getattr(slot_node, slot_node_attr_name)
        return slot_attrs

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        # <slot name='default'>
        slot_labels = slots.get('default', [])
        slot_label_node = slot_labels[0] if slot_labels else None
        if slot_label_node:
            attrs['name'] = slot_label_node.outer_html

        # <slot name='icon'>
        icon_slot: INode = slots.get('icon')
        if icon_slot:
            attrs['icon'] = icon_slot.inner_html

        # <slot name='active-icon'>
        active_icon_slot: INode = slots.get('active-icon')
        if active_icon_slot:
            attrs['active_icon'] = active_icon_slot.inner_html

        _params = {**props, **attrs, **params}
        if self._cls is None:
            raise ValueError(f"{self._cls.__name__} is not supported in this version of Panel")

        w = self._cls(**_params)

        if slot_label_node:
            def _update_button_name(change):
                val = change['new'] if isinstance(change, dict) else change
                w.name = val

            slot_label_node.on_change(_update_button_name)

        return w


@vpanel.ns_register()
class ButtonIcon(ActiveIconComponent):
    _cls = _ButtonIcon


@vpanel.ns_register()
class CheckBoxGroup(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('inline', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.CheckBoxGroup(**_params)


@vpanel.ns_register()
class CheckButtonGroup(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.CheckButtonGroup(**_params)


@vpanel.ns_register()
class Checkbox(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.Checkbox(**_params)


@vpanel.ns_register()
class CodeEditor(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('readonly', False),
        ('on_keyup', True),
        ('soft_tabs', False),
        ('print_margin', False),
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension('codeeditor')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.CodeEditor(**_params)


@vpanel.ns_register()
class ColorMap(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.ColorMap(**_params)


@vpanel.ns_register()
class ColorPicker(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.ColorPicker(**_params)


@vpanel.ns_register()
class CrossSelector(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('definition_order', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.CrossSelector(**_params)


# @vpanel.ns_register()
# class DataFrame(VPanelComponent):
#     v_model_default = 'value'
#     PARAMS_STORE_TRUE = [
#         ('disabled', False),
#         ('show_index', True),
#         ('auto_edit', False),
#     ]

#     def _render(self, ctx, attrs, props, params, setup_returned):
#         _params = {**props, **attrs, **params}
#         return pn.widgets.DataFrame(**_params)


@vpanel.ns_register()
class DatePicker(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.DatePicker(**_params)


@vpanel.ns_register()
class DateRangePicker(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.DateRangePicker(**_params)


@vpanel.ns_register()
class DateRangeSlider(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('show_value', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.DateRangeSlider(**_params)


@vpanel.ns_register()
class DateSlider(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('show_value', True),
        ('tooltips', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.DateSlider(**_params)


# todo
@vpanel.ns_register()
class DatetimeInput(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.DatetimeInput(**_params)


@vpanel.ns_register()
class DatetimePicker(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('enable_time', True),
        ('enable_seconds', True),
        ('military_time', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.DatetimePicker(**_params)


# todo
@vpanel.ns_register()
class DatetimeRangeInput(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.DatetimeRangeInput(**_params)


@vpanel.ns_register()
class DatetimeRangePicker(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.DatetimeRangePicker(**_params)


@vpanel.ns_register()
class DatetimeRangeSlider(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('show_value', True),
        ('tooltips', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.DatetimeRangeSlider(**_params)


@vpanel.ns_register()
class DatetimeSlider(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('show_value', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.DatetimeSlider(**_params)


@vpanel.ns_register()
class Debugger(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.Debugger(**_params)


@vpanel.ns_register()
class DiscretePlayer(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('show_loop_controls', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.DiscretePlayer(**_params)


@vpanel.ns_register()
class DiscreteSlider(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('show_value', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.DiscreteSlider(**_params)


class DisplayWidget(pn.Column):
    def __init__(self, obj, *args, **kwargs):
        super().__init__(obj, *args, **kwargs)

    @property
    def obj(self):
        return self[0]

    @obj.setter
    def obj(self, value):
        self[0] = pn.panel(value)


@vpanel.ns_register()
class Display(VPanelComponent):
    v_model_default = 'obj'
    PARAMS_STORE_TRUE = [
        ('scroll', False),
        ('view_latest', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        obj = _params.pop('obj')
        w = DisplayWidget(obj, **_params)
        return w


@vpanel.ns_register()
class EditableFloatSlider(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('tooltips', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.EditableFloatSlider(**_params)


@vpanel.ns_register()
class EditableIntSlider(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('tooltips', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.EditableIntSlider(**_params)


@vpanel.ns_register()
class EditableRangeSlider(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.EditableRangeSlider(**_params)


@vpanel.ns_register()
class FileDownload(VPanelComponent):
    v_model_default = 'filename'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('auto', True),
        ('embed', False),
    ]

    def _convert_slot_nodes_to_widgets(self, slots: Dict | None):
        pass

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        # <slot name='icon'>
        icon_slot: INode = slots.get('icon')
        if icon_slot:
            attrs['icon'] = icon_slot.inner_html

        _params = {**props, **attrs, **params}
        return pn.widgets.FileDownload(**_params)


@vpanel.ns_register()
class FileDropper(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('multiple', False),
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension('filedropper')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.FileDropper(**_params)


@vpanel.ns_register()
class FileInput(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('multiple', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.FileInput(**_params)


@vpanel.ns_register()
class FileSelector(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('only_files', False),
        ('show_hidden', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.FileSelector(**_params)


@vpanel.ns_register()
class FloatInput(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.FloatInput(**_params)


@vpanel.ns_register()
class FloatSlider(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('show_value', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.FloatSlider(**_params)


@vpanel.ns_register()
class Grammar(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.Grammar(**_params)


@vpanel.ns_register()
class GrammarList(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.GrammarList(**_params)


@vpanel.ns_register()
class IntInput(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.IntInput(**_params)


@vpanel.ns_register()
class IntRangeSlider(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('show_value', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.IntRangeSlider(**_params)


@vpanel.ns_register()
class IntSlider(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('show_value', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.IntSlider(**_params)


@vpanel.ns_register()
class JSONEditor(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension('ace', 'jsoneditor')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.JSONEditor(**_params)


@vpanel.ns_register()
class LiteralInput(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.LiteralInput(**_params)


@vpanel.ns_register()
class MenuButton(ButtonComponent):
    _cls = pn.widgets.MenuButton
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('split', False),
    ]


@vpanel.ns_register()
class MultiChoice(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('solid', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.MultiChoice(**_params)


@vpanel.ns_register()
class MultiSelect(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.MultiSelect(**_params)


@vpanel.ns_register()
class NestedSelect(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]
    LAYOUT_MAP = {
        'column': pn.Column,
        'row': pn.Row,
        'grid': pn.GridBox,
        'accordion': pn.Accordion,
    }

    def _process_layout(self, layout):
        if isinstance(layout, str):
            return self.LAYOUT_MAP[layout]

        return layout

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        layout = _params.pop('layout', 'column')
        _params['layout'] = self._process_layout(layout)
        return pn.widgets.NestedSelect(**_params)


@vpanel.ns_register()
class NumberInput(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.NumberInput(**_params)


@vpanel.ns_register()
class PasswordInput(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.PasswordInput(**_params)


@vpanel.ns_register()
class Player(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('show_value', False),
        ('show_loop_controls', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.Player(**_params)


@vpanel.ns_register()
class RadioBoxGroup(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('inline', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.RadioBoxGroup(**_params)


@vpanel.ns_register()
class RadioButtonGroup(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.RadioButtonGroup(**_params)


@vpanel.ns_register()
class RangeSlider(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('show_value', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.RangeSlider(**_params)


@vpanel.ns_register()
class Select(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.Select(**_params)


@vpanel.ns_register()
class SpeechToText(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('continuous', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.SpeechToText(**_params)


@vpanel.ns_register()
class Spinner(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.Spinner(**_params)


@vpanel.ns_register()
class StaticText(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.StaticText(**_params)


@vpanel.ns_register()
class Switch(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.Switch(**_params)


@vpanel.ns_register()
class Tabulator(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('show_index', True),
        ('hierarchical', False),
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension('tabulator')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.Tabulator(**_params)


@vpanel.ns_register()
class Terminal(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension('terminal')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.Terminal(**_params)


@vpanel.ns_register()
class TextAreaInput(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('auto_grow', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.TextAreaInput(**_params)


@vpanel.ns_register()
class TextEditor(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('toolbar', True),
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension('texteditor')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.TextEditor(**_params)


@vpanel.ns_register()
class TextInput(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.TextInput(**_params)


@vpanel.ns_register()
class TextToSpeech(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('auto_speak', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.TextToSpeech(**_params)


@vpanel.ns_register()
class TimePicker(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.TimePicker(**_params)


@vpanel.ns_register()
class Toggle(ButtonComponent):
    _cls = pn.widgets.Toggle
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]


@vpanel.ns_register()
class ToggleGroup(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.ToggleGroup(**_params)


@vpanel.ns_register()
class ToggleIcon(ActiveIconComponent):
    _cls = _ToggleIcon
    v_model_default = 'value'


@vpanel.ns_register()
class Utterance(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.Utterance(**_params)


@vpanel.ns_register()
class VideoStream(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('paused', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.VideoStream(**_params)


@vpanel.ns_register()
class Voice(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.Voice(**_params)
