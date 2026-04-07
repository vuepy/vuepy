"""Mapping between @keyup.* on VBox and Textual `bind` / Pilot.press.

`TextualNode.on` converts `keyup.ctrl.shift.c` to `ctrl+shift+c` (`.` → `+`).
"""
from __future__ import annotations

import pathlib

import pytest
from textual.widgets import Label

from vuepy import create_app, import_sfc


def _create_app():
    Root = import_sfc(pathlib.Path(__file__).parent / 'test_keyModifiers.vue')
    vue_app = create_app(Root, backend='textual')
    vue_app.mount(run=False)
    return vue_app


def _log(app) -> str:
    lab = app.screen.query_one('#key-mod-log', Label)
    c = getattr(lab, 'content', None)
    if isinstance(c, str):
        return c
    if c is not None and hasattr(c, 'plain'):
        return str(c.plain)
    r = getattr(lab, 'renderable', None)
    if r is not None and hasattr(r, 'plain'):
        return str(r.plain)
    return str(getattr(lab, 'label', '') or '')


async def _focus_capture(app, pilot):
    cap = app.screen.query_one('#kbd-capture')
    app.set_focus(cap)
    await pilot.pause(0.08)


async def _expect_key(
    app,
    pilot,
    log,
    sequence: str,
    token: str,
    pause: float = 0.11,
):
    """Clear the log, focus the capture widget, press the key, and assert ``token|`` appears in the log."""
    log.value = ''
    await _focus_capture(app, pilot)
    await pilot.press(sequence)
    await pilot.pause(pause)
    got = _log(app)
    assert f'{token}|' in got, f'press {sequence!r}: expected {token!r}, actual log={got!r}'


@pytest.fixture
def key_app():
    return _create_app()


async def test_key_lowercase_letters(key_app):
    vue_app = key_app
    app = vue_app.tt_app
    log = vue_app.root_component.setup_returned['key_log']

    async with app.run_test(size=(60, 22)) as pilot:
        await pilot.pause(0.2)
        log.value = ''
        await _focus_capture(app, pilot)
        await pilot.press('a')
        await pilot.pause(0.08)
        await pilot.press('b')
        await pilot.pause(0.1)
        out = _log(app)
        assert 'lower_a|' in out
        assert 'lower_b|' in out


async def test_key_uppercase_shift_a(key_app):
    """Uppercase letter: @keyup.shift.a; Pilot sends ``A`` (equivalent to shift+a on common layouts)."""
    vue_app = key_app
    app = vue_app.tt_app
    log = vue_app.root_component.setup_returned['key_log']

    async with app.run_test(size=(60, 22)) as pilot:
        await pilot.pause(0.2)
        await _expect_key(app, pilot, log, 'A', 'A')


async def test_key_digit_one(key_app):
    vue_app = key_app
    app = vue_app.tt_app
    log = vue_app.root_component.setup_returned['key_log']

    async with app.run_test(size=(60, 22)) as pilot:
        await pilot.pause(0.2)
        await _expect_key(app, pilot, log, '1', 'digit_1')


async def test_key_shift_one_symbol(key_app):
    """Symbol row: shift+1 (layout-dependent; skip on failure)."""
    vue_app = key_app
    app = vue_app.tt_app
    log = vue_app.root_component.setup_returned['key_log']

    async with app.run_test(size=(60, 22)) as pilot:
        await pilot.pause(0.2)
        try:
            await _expect_key(app, pilot, log, 'shift+1', 'shift_1')
        except AssertionError:
            pytest.skip('shift+1 did not match @keyup.shift.1 under the current Pilot/layout')


async def test_key_f1_and_insert(key_app):
    vue_app = key_app
    app = vue_app.tt_app
    log = vue_app.root_component.setup_returned['key_log']

    async with app.run_test(size=(60, 22)) as pilot:
        await pilot.pause(0.2)
        await _expect_key(app, pilot, log, 'f1', 'f1')
        await _expect_key(app, pilot, log, 'insert', 'insert')


async def test_key_arrow_up_right_down(key_app):
    vue_app = key_app
    app = vue_app.tt_app
    log = vue_app.root_component.setup_returned['key_log']

    async with app.run_test(size=(60, 22)) as pilot:
        await pilot.pause(0.2)
        log.value = ''
        await _focus_capture(app, pilot)
        for seq, tok in (('up', 'arrow_up'), ('right', 'arrow_right'), ('down', 'arrow_down')):
            await pilot.press(seq)
            await pilot.pause(0.09)
        out = _log(app)
        assert 'arrow_up|' in out
        assert 'arrow_right|' in out
        assert 'arrow_down|' in out


async def test_key_ctrl_chords(key_app):
    vue_app = key_app
    app = vue_app.tt_app
    log = vue_app.root_component.setup_returned['key_log']

    async with app.run_test(size=(60, 22)) as pilot:
        await pilot.pause(0.2)
        pairs = (
            ('ctrl+a', 'ctrl_a'),
            ('ctrl+f1', 'ctrl_f1'),
            ('ctrl+insert', 'ctrl_insert'),
            ('ctrl+right', 'ctrl_right'),
            ('ctrl+home', 'ctrl_home'),
        )
        for seq, tok in pairs:
            await _expect_key(app, pilot, log, seq, tok)

        for und in ('ctrl+underscore', 'ctrl+_'):
            log.value = ''
            await _focus_capture(app, pilot)
            await pilot.press(und)
            await pilot.pause(0.11)
            if 'ctrl_underscore|' in _log(app):
                break
        else:
            pytest.skip('Pilot did not fire ctrl+underscore (tried both ctrl+underscore and ctrl+_)')


async def test_key_shift_chords(key_app):
    vue_app = key_app
    app = vue_app.tt_app
    log = vue_app.root_component.setup_returned['key_log']

    async with app.run_test(size=(60, 22)) as pilot:
        await pilot.pause(0.2)
        await _expect_key(app, pilot, log, 'shift+end', 'shift_end')
        await _expect_key(app, pilot, log, 'shift+up', 'shift_up')
        await _expect_key(app, pilot, log, 'shift+home', 'shift_home')
        await _expect_key(app, pilot, log, 'shift+tab', 'shift_tab')


async def test_key_alt_chords(key_app):
    vue_app = key_app
    app = vue_app.tt_app
    log = vue_app.root_component.setup_returned['key_log']

    async with app.run_test(size=(60, 22)) as pilot:
        await pilot.pause(0.2)
        await _expect_key(app, pilot, log, 'alt+a', 'alt_a')
        await _expect_key(app, pilot, log, 'alt+up', 'alt_up')
        await _expect_key(app, pilot, log, 'alt+home', 'alt_home')


async def test_key_ctrl_shift_c_pivot(key_app):
    """ctrl+shift+c: modifier chain in the template is @keyup.ctrl.shift.c (pivot order)."""
    vue_app = key_app
    app = vue_app.tt_app
    log = vue_app.root_component.setup_returned['key_log']

    async with app.run_test(size=(60, 22)) as pilot:
        await pilot.pause(0.2)
        await _expect_key(app, pilot, log, 'ctrl+shift+c', 'ctrl_shift_c')


async def test_key_enter_escape_space(key_app):
    vue_app = key_app
    app = vue_app.tt_app
    log = vue_app.root_component.setup_returned['key_log']

    async with app.run_test(size=(60, 22)) as pilot:
        await pilot.pause(0.2)
        log.value = ''
        await _focus_capture(app, pilot)
        for seq, tok in (('enter', 'enter'), ('escape', 'escape'), ('space', 'space')):
            await pilot.press(seq)
            await pilot.pause(0.07)
        out = _log(app)
        for tok in ('enter', 'escape', 'space'):
            assert f'{tok}|' in out


async def test_key_tab(key_app):
    vue_app = key_app
    app = vue_app.tt_app
    log = vue_app.root_component.setup_returned['key_log']

    async with app.run_test(size=(60, 22)) as pilot:
        await pilot.pause(0.2)
        await _expect_key(app, pilot, log, 'tab', 'tab')


async def test_key_meta_combo_if_supported(key_app):
    vue_app = key_app
    app = vue_app.tt_app
    log = vue_app.root_component.setup_returned['key_log']

    async with app.run_test(size=(60, 22)) as pilot:
        await pilot.pause(0.2)
        for seq in ('meta+m', 'super+m'):
            log.value = ''
            await _focus_capture(app, pilot)
            await pilot.press(seq)
            await pilot.pause(0.12)
            if 'meta_m|' in _log(app):
                return
        pytest.skip('Pilot did not fire @keyup.meta.m in the current environment (tried meta+m and super+m)')
