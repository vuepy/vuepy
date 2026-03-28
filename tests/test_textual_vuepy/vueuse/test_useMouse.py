"""`textual_vuepy.vueuse.useMouse`: consistent with `ev.screen_x` / `ev.screen_y`, returns **screen coordinates** (not widget-local coordinates).

Textual Pilot: `hover(None, offset=(x, y))` means coordinates relative to the **current screen area**;
`hover(widget, offset=(dx, dy))` ultimately `screen_x/y = widget.region.offset + offset`.
"""
from __future__ import annotations

import pathlib

from textual.widgets import Button, Label

from vuepy import create_app, import_sfc


def _create_use_mouse_app():
    Root = import_sfc(pathlib.Path(__file__).parent / 'test_useMouse.vue')
    vue_app = create_app(Root, backend='textual')
    vue_app.mount(run=False)
    return vue_app.tt_app


def _parse_xy(s: str) -> tuple[int, int]:
    s = s.strip().replace(' ', '')
    a, b = s.split(',', 1)
    return int(a), int(b)


def _read_xy_label(lab: Label) -> tuple[int, int]:
    return _parse_xy(lab.content.strip())


async def test_use_mouse_matches_pilot_screen_offset():
    """
    When no widget is passed, offset is relative to the screen; 
    Label should match screen_x/screen_y injected by Pilot.
    """
    app = _create_use_mouse_app()
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.pause(0.2)
        xy_label = app.screen.query_one('#mouse-xy', Label)

        await pilot.hover(None, offset=(14, 9))
        await pilot.pause(0.15)
        assert _read_xy_label(xy_label) == (14, 9)

        await pilot.hover(None, offset=(55, 16))
        await pilot.pause(0.15)
        assert _read_xy_label(xy_label) == (55, 16)


async def test_use_mouse_widget_hover_is_screen_region_plus_offset():
    """Widget-relative hover is converted to screen coordinates by Pilot; useMouse should display the converted value.

    The layout must ensure the button's `region.offset` is not (0,0): a wrong implementation that
    only uses widget-relative offset would yield (7,4) for offset=(7,4), while the correct screen
    coordinate should be (ox+7, oy+4); they differ when ox or oy is non-zero.
    """
    app = _create_use_mouse_app()
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.pause(0.2)
        xy_label = app.screen.query_one('#mouse-xy', Label)
        btn = app.screen.query_one('#hover-target', Button)

        ox = btn.region.offset.x
        oy = btn.region.offset.y
        assert (ox, oy) != (0, 0), (
            'test_useMouse.vue must use spacer/margin to ensure #hover-target screen offset is not (0,0); '
            'otherwise screen coordinates and widget-local coordinates cannot be distinguished'
        )

        await pilot.hover(btn, offset=(0, 0))
        await pilot.pause(0.15)
        assert _read_xy_label(xy_label) == (ox, oy)

        dx, dy = 7, 4
        await pilot.hover(btn, offset=(dx, dy))
        await pilot.pause(0.15)
        assert _read_xy_label(xy_label) == (ox + dx, oy + dy)
        assert _read_xy_label(xy_label) != (dx, dy)
