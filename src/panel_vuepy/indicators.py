# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
import panel as pn

from panel_vuepy.core import VPanelComponent, vpanel


@vpanel.ns_register()
class BooleanStatus(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.BooleanStatus(**_params)


@vpanel.ns_register()
class Dial(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.Dial(**_params)


@vpanel.ns_register()
class Gauge(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _load_extension(cls):
        pn.extension('echarts')

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.Gauge(**_params)


@vpanel.ns_register()
class LinearGauge(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('show_boundaries', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.LinearGauge(**_params)


@vpanel.ns_register()
class LoadingSpinner(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.LoadingSpinner(**_params)


@vpanel.ns_register()
class Number(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.Number(**_params)


@vpanel.ns_register()
class Progress(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
        ('active', True),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.Progress(**_params)


@vpanel.ns_register()
class TooltipIcon(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.TooltipIcon(**_params)


@vpanel.ns_register()
class Tqdm(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.Tqdm(**_params)


@vpanel.ns_register()
class Trend(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('disabled', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.widgets.Trend(**_params)
