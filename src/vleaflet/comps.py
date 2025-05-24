from ipywidgets import VBox
import ipyleaflet

from vleaflet.core import IPyLeafletComponent, leaflet


@leaflet.ns_register()
class Map(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {
            **props,
            **attrs,
        }
        map_widget = ipyleaflet.Map(
            **{k.replace('-', '_'): v for k, v in _params.items()},
        )

        layers = getattr(slots.get('layers', []), 'children', [])
        controls = getattr(slots.get('controls', []), 'children', [])
        for layer in layers:
            map_widget.add_layer(layer)
        for control in controls:
            map_widget.add_control(control)

        return map_widget


@leaflet.ns_register()
class Marker(IPyLeafletComponent):
    v_model_default = 'location'

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}
        icon = slots.get('icon')
        if icon and len(icon.children) > 0:
            _params['icon'] = icon.children[0]

        m = ipyleaflet.Marker(**_params)

        popup = slots.get('popup')
        if popup:
            m.popup = popup

        return m


@leaflet.ns_register()
class WidgetControl(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        widgets = slots.get('default')
        if widgets:
            widgets = widgets[0] if len(widgets) == 1 else VBox(widgets)

        control = ipyleaflet.WidgetControl(
            widget=widgets,
            **{k.replace('-', '_'): v for k, v in props.items()},
            **attrs
        )

        return control


@leaflet.ns_register()
class ZoomControl(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.ZoomControl(**props, **attrs)


@leaflet.ns_register()
class ScaleControl(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.ScaleControl(**props, **attrs)


@leaflet.ns_register()
class LayersControl(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.LayersControl(**props, **attrs)


@leaflet.ns_register()
class FullscreenControl(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return ipyleaflet.FullScreenControl(**_params)


@leaflet.ns_register()
class MeasureControl(IPyLeafletComponent):
    # todo 如何获取标记的点？
    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        _params.setdefault("primary_length_unit", 'meters')
        _params.setdefault("primary_area_unit", 'sqmeters')
        return ipyleaflet.MeasureControl(**_params)


@leaflet.ns_register()
class SplitMapControl(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots')
        left = getattr(slots.get('left', []), 'children', [None])[0]
        right = getattr(slots.get('right', []), 'children', [None])[0]
        _params = {**props, **attrs, **params, 'left_layer': left, 'right_layer': right}
        return ipyleaflet.SplitMapControl(**_params)


@leaflet.ns_register()
class GeomanDrawControl(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.GeomanDrawControl(**props, **attrs)


@leaflet.ns_register()
class LegendControl(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.LegendControl(**props, **attrs)


@leaflet.ns_register()
class SearchControl(IPyLeafletComponent):
    # todo search layers, put onmounted

    def _render(self, ctx, attrs, props, params, setup_returned):
        default_slot = ctx.get('slots', {}).get('default')
        _params = {**props, **attrs, **params}
        if default_slot:
            _params['marker'] = default_slot[0]

        return ipyleaflet.SearchControl(**_params)


@leaflet.ns_register()
class TileLayer(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.TileLayer(**props, **attrs)


@leaflet.ns_register()
class ImageOverlay(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.ImageOverlay(**props, **attrs)


@leaflet.ns_register()
class ImageService(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.ImageService(**props, **attrs)


@leaflet.ns_register()
class VideoOverlay(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.VideoOverlay(**props, **attrs)


@leaflet.ns_register()
class LocalTileLayer(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.LocalTileLayer(**props, **attrs)


@leaflet.ns_register()
class MarkerCluster(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        widgets = slots.get('default')
        _params = {**props, **attrs, **params}
        if widgets:
            _params['markers'] = widgets

        return ipyleaflet.MarkerCluster(**_params)


@leaflet.ns_register()
class Polyline(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.Polyline(**props, **attrs)


@leaflet.ns_register()
class Polygon(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.Polygon(**props, **attrs)


@leaflet.ns_register()
class Rectangle(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.Rectangle(**props, **attrs)


@leaflet.ns_register()
class Circle(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.Circle(**props, **attrs)


@leaflet.ns_register()
class CircleMarker(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.CircleMarker(**props, **attrs)


@leaflet.ns_register()
class GeoJson(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.GeoJSON(**props, **attrs)


@leaflet.ns_register()
class GeoData(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.GeoData(**props, **attrs)


@leaflet.ns_register()
class Choropleth(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.Choropleth(**props, **attrs)


@leaflet.ns_register()
class LayerGroup(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        widgets = slots.get('default')
        _params = {**props, **attrs, **params}
        if widgets:
            _params['layers'] = widgets

        return ipyleaflet.LayerGroup(**_params)


@leaflet.ns_register()
class Heatmap(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.Heatmap(**props, **attrs)


@leaflet.ns_register()
class Icon(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.Icon(**props, **attrs)


@leaflet.ns_register()
class AwesomeIcon(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.AwesomeIcon(**props, **attrs)


@leaflet.ns_register()
class DivIcon(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        html = slots.get('default')
        _params = {**props, **attrs, **params}
        if html:
            html = html[0]
            _params['html'] = html.value

        icon = ipyleaflet.DivIcon(**_params)

        if html:
            def _update_icon_html(val):
                # todo make dynamic
                icon.html = val

            html.on_change(_update_icon_html)

        return icon


@leaflet.ns_register()
class Popup(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        widgets = slots.get('default')
        _params = {**props, **attrs, **params}
        if widgets:
            widgets = widgets[0] if len(widgets) == 1 else VBox(widgets)
            _child_param = _params.get('child')
            if isinstance(_child_param, (list, tuple)):
                widgets.extend(_child_param)

            _params['child'] = widgets

        return ipyleaflet.Popup(**_params)


@leaflet.ns_register()
class AntPath(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.AntPath(**props, **attrs)


@leaflet.ns_register()
class Velocity(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.Velocity(**props, **attrs)


@leaflet.ns_register()
class WmsLayer(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.WMSLayer(**props, **attrs)


@leaflet.ns_register()
class MagnifyingGlass(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        default_slot = ctx.get('slots', {}).get('default')
        _params = {**props, **attrs, **params}
        if default_slot:
            _params['layers'] = default_slot

        return ipyleaflet.MagnifyingGlass(**_params)


@leaflet.ns_register()
class VectorTileLayer(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.VectorTileLayer(**props, **attrs)


@leaflet.ns_register()
class WktLayer(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.WKTLayer(**props, **attrs)

