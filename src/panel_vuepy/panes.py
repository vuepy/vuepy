# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
# 参考 @comps.py @comps.py 为python panel库的AutocompleteInput,BooleanStatus,ButtonIcon,
# CheckBoxGroup,CheckButtonGroup,Checkbox,CodeEditor,ColorMap,ColorPicker,
# CompositeWidget,CrossSelector,DataFrame 编写组件，保存到 @comps.py 中，一次性生成所有组件
from __future__ import annotations
from types import MethodType
from typing import Dict

import panel as pn

from panel_vuepy.core import VPanelComponent, vpanel
from vuepy.compiler_sfc.codegen_backends.panel import CollectionRootWidget


# todo markdown
@vpanel.ns_register()
class Alert(VPanelComponent):
    v_model_default = 'active'
    PARAMS_STORE_TRUE = [
    ]

    def _convert_slot_nodes_to_widgets(self, slots: Dict | None):
        pass

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}
        # <slot name='default'>
        slot_labels = slots.get('default', [])
        slot_label_node = slot_labels[0] if slot_labels else None
        slot_value = ''
        if slot_label_node:
            slot_value = slot_label_node.outer_html
        
        _value = _params.pop(self.v_model_default, '')
        if _value and slot_value:
            raise ValueError(f'{self.v_model_default} and default slot cannot both be provided')

        w = pn.pane.Alert(slot_value or _value, **_params)
        # handle <slot name='default'> content change
        if slot_label_node:
            def _update_button_name(change):
                val = change['new'] if isinstance(change, dict) else change
                w.object = val

            slot_label_node.on_change(_update_button_name)

        return w


@vpanel.ns_register()
class Audio(VPanelComponent):
    v_model_default = 'src'
    PARAMS_STORE_TRUE = [
        ('autoplay', False),
        ('loop', False),
        ('muted', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.Audio(**_params)


@vpanel.ns_register()
class Bokeh(VPanelComponent):
    v_model_default = 'plot'
    PARAMS_STORE_TRUE = [
        ('height', 400),
        ('width', 600),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.Bokeh(**_params)


@vpanel.ns_register()
class DataFrame(VPanelComponent):
    v_model_default = 'data'
    PARAMS_STORE_TRUE = [
        ('show_index', True),
        ('auto_edit', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.DataFrame(**_params)


@vpanel.ns_register()
class DeckGl(VPanelComponent):
    v_model_default = 'data'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.DeckGl(**_params)


@vpanel.ns_register()
class ECharts(VPanelComponent):
    EVENTS = [
        'click',
    ]
    JS_EVENTS = [
        'click',
    ]
    v_model_default = 'options'
    PARAMS_STORE_TRUE = [
        ('height', 400),
        ('width', 600),
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension('echarts')

    def _inject_on_event_register(self, event, widget):
        def on_ev(this, callback, remove=False):
            this.on_event(event, callback)

        setattr(widget, f'on_{event}', MethodType(on_ev, widget))

    def _inject_js_on_event_register(self, event, widget):
        def on_ev(this, callback, remove=False):
            this.js_on_event(event, callback())

        setattr(widget, f'on_js{event}', MethodType(on_ev, widget))

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        w = pn.pane.ECharts(**_params)
        for ev in self.EVENTS:
            self._inject_on_event_register(ev, w)
        for ev in self.JS_EVENTS:
            self._inject_js_on_event_register(ev, w)
        return w


@vpanel.ns_register()
class Folium(VPanelComponent):
    v_model_default = 'map'
    PARAMS_STORE_TRUE = [
        ('height', 400),
        ('width', 600),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.plot.Folium(**_params)


@vpanel.ns_register(name=['Gif', 'GIF'])
class Gif(VPanelComponent):
    v_model_default = 'object'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.GIF(**_params)


@vpanel.ns_register()
class HTML(VPanelComponent):
    v_model_default = 'object'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        # value = _params.pop('value', '')
        return pn.pane.HTML(**_params)


@vpanel.ns_register()
class HoloViews(VPanelComponent):
    v_model_default = 'object'
    PARAMS_STORE_TRUE = [
        # ('center', False),
    ]

    @classmethod
    def _load_extension(cls):
        import holoviews as hv
        hv.extension('bokeh', 'plotly')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.HoloViews(**_params)


@vpanel.ns_register()
class IPyWidget(VPanelComponent):
    v_model_default = 'widget'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.IPyWidget(**_params)


@vpanel.ns_register()
class Image(VPanelComponent):
    v_model_default = 'object'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        # src = _params.pop('src', '')
        return pn.pane.Image(**_params)


@vpanel.ns_register(name=['Jpg', 'JPG'])
class Jpg(VPanelComponent):
    v_model_default = 'object'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.JPG(**_params)


@vpanel.ns_register(name=['Json', 'JSON'])
class Json(VPanelComponent):
    v_model_default = 'data'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.JSON(**_params)


@vpanel.ns_register(name=['Latex', 'LaTeX'])
class Latex(VPanelComponent):
    v_model_default = 'content'
    PARAMS_STORE_TRUE = [
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension('katex', 'mathjax')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.LaTeX(**_params)


@vpanel.ns_register(name=['Markdown', 'MD', 'Md'])
class Markdown(VPanelComponent):
    v_model_default = 'object'
    PARAMS_STORE_TRUE = [
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension("mathjax")

    def _convert_slot_nodes_to_widgets(self, slots: Dict | None):
        pass

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}
        # <slot name='default'>
        slot_labels = slots.get('default', [])
        slot_label_node = slot_labels[0] if slot_labels else None
        slot_value = ''
        if slot_label_node:
            slot_value = slot_label_node.outer_html
        
        _value = _params.pop(self.v_model_default, '')
        if _value and slot_value:
            raise ValueError(f'{self.v_model_default} and default slot cannot both be provided')

        w = pn.pane.Markdown(slot_value or _value, **_params)

        # handle <slot name='default'> content change
        if slot_label_node:
            def _update_button_name(change):
                val = change['new'] if isinstance(change, dict) else change
                w.object = val

            slot_label_node.on_change(_update_button_name)

        return w


@vpanel.ns_register()
class Matplotlib(VPanelComponent):
    v_model_default = 'plot'
    PARAMS_STORE_TRUE = [
        ('tight', False),
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension('ipywidgets')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.Matplotlib(**_params)


@vpanel.ns_register(name=['Pdf', 'PDF'])
class Pdf(VPanelComponent):
    v_model_default = 'object'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.PDF(**_params)


@vpanel.ns_register(name=['Png', 'PNG'])
class Png(VPanelComponent):
    v_model_default = 'object'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.PNG(**_params)


@vpanel.ns_register()
class Param(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        slots.pop('default', None)
        _params = {**props, **attrs, **params}

        if slots:
            widgets = {}
            for key, slot in slots.items():
                widgets[key] = (
                    slot.objects[0]
                    if isinstance(slot, CollectionRootWidget)
                    else slot
                )
            _params['widgets'] = widgets

        return pn.Param(**_params)


@vpanel.ns_register()
class Perspective(VPanelComponent):
    v_model_default = 'data'
    PARAMS_STORE_TRUE = [
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension('perspective')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.Perspective(**_params)


@vpanel.ns_register()
class Placeholder(VPanelComponent):
    v_model_default = 'object'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.Placeholder(**_params)


@vpanel.ns_register()
class Plotly(VPanelComponent):
    EVENTS = [
        'click', 'hover', 'selected', 'doubleclick', 'clickannotation',
        'relayout', 'restyle',
    ]
    v_model_default = 'object'
    PARAMS_STORE_TRUE = [
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension('plotly')

    def _inject_on_event_register(self, event, widget):
        def on_ev(this, callback, remove=False):
            attr = f"{event}_data"
            if remove:
                this.param.unwatch(callback, attr)
            else:
                this.param.watch(callback, attr)

        setattr(widget, f'on_{event}', MethodType(on_ev, widget))

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        w = pn.pane.Plotly(**_params)
        for ev in self.EVENTS:
            self._inject_on_event_register(ev, w)
        return w


@vpanel.ns_register()
class ReactiveExpr(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.ReactiveExpr(**_params)


@vpanel.ns_register()
class Reaction(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.Reaction(**_params)


@vpanel.ns_register(name=['Svg', 'SVG'])
class Svg(VPanelComponent):
    v_model_default = 'object'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.SVG(**_params)


@vpanel.ns_register()
class Str(VPanelComponent):
    v_model_default = 'object'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.Str(**_params)


@vpanel.ns_register()
class Streamz(VPanelComponent):
    v_model_default = 'data'
    PARAMS_STORE_TRUE = [
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension('vega')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.Streamz(**_params)


@vpanel.ns_register()
class Textual(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension('terminal')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.Textual(**_params)


@vpanel.ns_register(name=['VTK', 'Vtk'])
class Vtk(VPanelComponent):
    v_model_default = 'object'
    PARAMS_STORE_TRUE = []

    @classmethod
    def _load_extension(cls):
        pn.extension("vtk")

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        object = _params.pop('object')
        return pn.pane.VTK(object, **_params)


@vpanel.ns_register(name=['VTKVolume', 'VtkVolume'])
class VtkVolume(VPanelComponent):
    v_model_default = ''
    PARAMS_STORE_TRUE = [
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension("vtk")

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        object = _params.pop('object')
        return pn.pane.VTKVolume(object, **_params)


@vpanel.ns_register()
class Vega(VPanelComponent):
    v_model_default = 'spec'
    PARAMS_STORE_TRUE = [
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension("vega")

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.Vega(**_params)


@vpanel.ns_register()
class Video(VPanelComponent):
    v_model_default = 'time'
    PARAMS_STORE_TRUE = [
        ('autoplay', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.Video(**_params)


@vpanel.ns_register()
class Vizzu(VPanelComponent):
    v_model_default = 'object'
    PARAMS_STORE_TRUE = [
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension('vizzu')

    def _process_style(self, kw):
        pass

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.Vizzu(**_params)


@vpanel.ns_register(name=['Webp', 'WebP'])
class Webp(VPanelComponent):
    v_model_default = 'object'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.pane.WebP(**_params)
