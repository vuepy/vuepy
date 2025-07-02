# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
import panel as pn

from panel_vuepy.core import VPanelComponent, vpanel


@vpanel.ns_register()
class Accordion(VPanelComponent):
    v_model_default = 'active'
    PARAMS_STORE_TRUE = [
        ('toggle', False),
        ('scroll', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}
        children = slots.get('default', [])
        # # Extract titles from AccordionItem children
        # _children = []
        # for child in children:
        #     if hasattr(child, 'title'):
        #         _children.append((child.title, child))
        #     else:
        #         _children.append(child)

        return pn.Accordion(*children, **_params)


@vpanel.ns_register()
class AccordionItem(VPanelComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}
        children = slots.get('default', [])
        # title = _params.pop('title', None)

        # Create a Column for the accordion item content
        widget = pn.Column(*children, **_params)
        # Store the title for Accordion parent to use
        # if title:
        #     widget.title = title
        return widget


@vpanel.ns_register()
class Card(VPanelComponent):
    PARAMS_STORE_TRUE = [
        ('collapsible', True),
        ('collapsed', False),
        ('hide_header', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}

        header = slots.get('header', [])
        if header:
            _params['header'] = header[0]

        default_content = slots.get('default', [])

        card = pn.Card(*default_content, **_params)
        return card


@vpanel.ns_register()
class Divider(VPanelComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        return pn.layout.Divider(**_params)


@vpanel.ns_register()
class Feed(VPanelComponent):
    v_model_default = 'posts'
    PARAMS_STORE_TRUE = [
        ('scroll', True),
        ('view_latest', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}
        children = slots.get('default', [])
        return pn.Feed(*children, **_params)


@vpanel.ns_register()
class FlexBox(VPanelComponent):
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}
        children = slots.get('default', [])

        # # Extract sizing_mode or direction from props
        # sizing_mode = _params.pop('sizing_mode', 'stretch_width')
        # direction = _params.pop('direction', 'row')

        return pn.FlexBox(*children, **_params)


@vpanel.ns_register()
class FloatPanel(VPanelComponent):
    v_model_default = 'status'
    PARAMS_STORE_TRUE = [
        ('contained', True),
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension('floatpanel')

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}
        children = slots.get('default', [])

        # Extract position props
        # position = _params.pop('position', 'right')

        return pn.FloatPanel(*children, **_params)


@vpanel.ns_register()
class GridBox(VPanelComponent):
    PARAMS_STORE_TRUE = [
        ('scroll', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}
        children = slots.get('default', [])

        # Extract grid-specific props
        ncols = _params.pop('ncols', None)
        nrows = _params.pop('nrows', None)

        return pn.GridBox(*children, ncols=ncols, nrows=nrows, **_params)


@vpanel.ns_register()
class GridSpec(VPanelComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}

        # Create GridSpec
        # grid = pn.GridSpec(nrows=nrows, ncols=ncols, **_params)
        grid = pn.GridSpec(**_params)

        # Process child elements with their grid positions
        children = slots.get('default', [])
        for child in children:
            if hasattr(child, 'grid_position'):
                row_start, row_end, col_start, col_end = child.grid_position
                grid[row_start:row_end, col_start:col_end] = child

        return grid


@vpanel.ns_register()
class GridSpecItem(VPanelComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}

        # Extract grid position information
        row_start = _params.pop('row_start', 0)
        row_end = _params.pop('row_end', row_start + 1)
        col_start = _params.pop('col_start', 0)
        col_end = _params.pop('col_end', col_start + 1)

        # Create container for content
        children = slots.get('default', [])
        container = pn.Column(*children, **_params)

        # Store grid position for parent GridSpec to use
        container.grid_position = (row_start, row_end, col_start, col_end)

        return container


@vpanel.ns_register()
class GridStack(VPanelComponent):
    PARAMS_STORE_TRUE = [
        ('allow_resize', True),
        ('allow_drag', True),
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension('gridstack')

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}

        # Create GridStack
        # grid = pn.GridStack(ncols=ncols, **_params)
        grid = pn.GridStack(**_params)

        # Process child elements with their grid positions
        children = slots.get('default', [])
        for child in children:
            if hasattr(child, 'grid_position'):
                row_start, row_end, col_start, col_end = child.grid_position
                # grid[row_start:row_end, col_start:col_end] = child
                grid[row_start:row_end, col_start:col_end] = child.objects[0]

        return grid


@vpanel.ns_register()
class GridStackItem(GridSpecItem):
    pass


@vpanel.ns_register()
class Modal(VPanelComponent):
    v_model_default = 'open'
    PARAMS_STORE_TRUE = [
        ('scroll', False),
        ('open', False),
        ('show_close_button', True),
        ('background_close', True),
    ]

    @classmethod
    def _load_extension(cls):
        pn.extension('modal')

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}

        # Process slots for different modal sections
        header = slots.get('header', [])
        header_items = header[0] if header else None

        default_content = slots.get('default', [])
        footer = slots.get('footer', [])
        footer_items = footer[0] if footer else None

        # Create Modal
        modal = pn.Modal(*default_content, **_params)

        # Set header and footer if provided
        if header_items:
            modal.header = header_items
        if footer_items:
            modal.footer = footer_items

        return modal


@vpanel.ns_register()
class Spacer(VPanelComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}

        return pn.layout.Spacer(**_params)


@vpanel.ns_register()
class Swipe(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        _params = {**props, **attrs, **params}
        before = _params.pop('before', None)
        after = _params.pop('after', None)

        return pn.Swipe(before, after, **_params)


@vpanel.ns_register()
class SwipeItem(VPanelComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}
        title = _params.pop('title', None)
        children = slots.get('default', [])

        # Create container for swipe item content
        container = pn.Column(*children, **_params)
        if title:
            container.title = title

        return container


@vpanel.ns_register()
class Tabs(VPanelComponent):
    v_model_default = 'active'
    PARAMS_STORE_TRUE = [
        ('closable', False),
        ('dynamic', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}
        children = slots.get('default', [])

        # # Extract titles from TabPane children
        # titles = []
        # for child in children:
        #     if hasattr(child, 'title'):
        #         titles.append(child.title)
        #     else:
        #         titles.append('-')

        return pn.Tabs(*children, **_params)


@vpanel.ns_register()
class TabPane(VPanelComponent):
    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}
        # title = _params.pop('title', '-')
        children = slots.get('default', [])

        # Create a container for the tab content
        container = pn.Column(*children, **_params)
        # container.title = title

        return container


@vpanel.ns_register()
class WidgetBox(VPanelComponent):
    PARAMS_STORE_TRUE = [
        ('scroll', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}
        children = slots.get('default', [])

        return pn.WidgetBox(*children, **_params)


@vpanel.ns_register(name=['Column', 'Col'])
class Column(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('scroll', False),
        ('view_latest', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}
        children = slots.get('default', [])
        w = pn.Column(*children, **_params)
        return w


@vpanel.ns_register()
class Row(VPanelComponent):
    v_model_default = 'value'
    PARAMS_STORE_TRUE = [
        ('scroll', False),
    ]

    def _render(self, ctx, attrs, props, params, setup_returned):
        slots = ctx.get('slots', {})
        _params = {**props, **attrs, **params}
        children = slots.get('default', [])
        w = pn.Row(*children, **_params)
        return w
