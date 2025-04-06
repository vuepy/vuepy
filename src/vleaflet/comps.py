from ipywidgets import VBox
import ipyleaflet

from vleaflet.core import IPyLeafletComponent, leaflet


@leaflet.ns_register()
class Map(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})

        # # Basic parameters
        # center = props.get('center', [0, 0])
        # zoom = props.get('zoom', 10)

        # # Zoom related parameters
        # max_zoom = props.get('max_zoom')
        # min_zoom = props.get('min_zoom')
        # zoom_snap = props.get('zoom_snap', 1)
        # zoom_delta = props.get('zoom_delta', 1)

        # # Interaction related parameters
        # dragging = props.get('dragging', True)
        # touch_zoom = props.get('touch_zoom', True)
        # scroll_wheel_zoom = props.get('scroll_wheel_zoom', False)
        # double_click_zoom = props.get('double_click_zoom', True)
        # box_zoom = props.get('box_zoom', True)
        # tap = props.get('tap', True)
        # tap_tolerance = props.get('tap_tolerance', 15)
        # world_copy_jump = props.get('world_copy_jump', False)
        # close_popup_on_click = props.get('close_popup_on_click', True)
        # bounce_at_zoom_limits = props.get('bounce_at_zoom_limits', True)

        # # Keyboard control parameters
        # keyboard = props.get('keyboard', True)
        # keyboard_pan_offset = props.get('keyboard_pan_offset', 80)
        # keyboard_zoom_offset = props.get('keyboard_zoom_offset', 1)

        # # Inertia related parameters
        # inertia = props.get('inertia', True)
        # inertia_deceleration = props.get('inertia_deceleration', 3000)
        # inertia_max_speed = props.get('inertia_max_speed', 1500)

        # # Control related parameters
        # zoom_control = props.get('zoom_control', True)
        # attribution_control = props.get('attribution_control', True)
        # zoom_animation_threshold = props.get('zoom_animation_threshold', 4)

        # # Style related parameters
        # style = props.get('style', {})

        # Create map instance
        _params = {
            **props,
            **attrs,
        }
        map_widget = ipyleaflet.Map(
            **{k.replace('-', '_'): v for k, v in _params.items()},
            # center=center,
            # zoom=zoom,
            # max_zoom=max_zoom,
            # min_zoom=min_zoom,
            # zoom_snap=zoom_snap,
            # zoom_delta=zoom_delta,
            # dragging=dragging,
            # touch_zoom=touch_zoom,
            # scroll_wheel_zoom=scroll_wheel_zoom,
            # double_click_zoom=double_click_zoom,
            # box_zoom=box_zoom,
            # tap=tap,
            # tap_tolerance=tap_tolerance,
            # world_copy_jump=world_copy_jump,
            # close_popup_on_click=close_popup_on_click,
            # bounce_at_zoom_limits=bounce_at_zoom_limits,
            # keyboard=keyboard,
            # keyboard_pan_offset=keyboard_pan_offset,
            # keyboard_zoom_offset=keyboard_zoom_offset,
            # inertia=inertia,
            # inertia_deceleration=inertia_deceleration,
            # inertia_max_speed=inertia_max_speed,
            # zoom_control=zoom_control,
            # attribution_control=attribution_control,
            # zoom_animation_threshold=zoom_animation_threshold,
            # **style
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
        _params = {**props, **attrs}
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
class FullScreenControl(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs}
        _params.setdefault('primary_length_unit', 'meters')
        _params.setdefault('primary_area_unit', 'sqmeters')
        return ipyleaflet.FullScreenControl(**_params)


@leaflet.ns_register()
class MeasureControl(IPyLeafletComponent):
    # todo 如何获取标记的点？
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.MeasureControl(**props, **attrs)


@leaflet.ns_register()
class SplitMapControl(IPyLeafletComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        return ipyleaflet.SplitMapControl(**props, **attrs)


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
    # todo search layers

    def _render(self, ctx, attrs, props, params, setup_returned):
        default_slot = ctx.get('slots', {}).get('default')
        _params = {**props, **attrs}
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
        _params = {**props, **attrs}
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
        _params = {**props, **attrs}
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
        _params = {**props, **attrs}
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
        _params = {**props, **attrs}
        if widgets:
            widgets = widgets[0] if len(widgets) == 1 else vbox(widgets)
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
        _params = {**props, **attrs}
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

