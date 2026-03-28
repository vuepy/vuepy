"""`<component :is=\"...\">` dynamic component (see `vuepy` DynamicComponent / template_codegen).

See `src/textual_vuepy/_research/test_component.py`.
"""
from __future__ import annotations

import pathlib
import re

import pytest
from textual.widgets import Button, Label

from vuepy import create_app, import_sfc


def _create_app():
    Root = import_sfc(pathlib.Path(__file__).parent / 'test_dynamic_component.vue')
    vue_app = create_app(Root, backend='textual')
    vue_app.mount(run=False)
    return vue_app


def _static_text(widget) -> str:
    content = getattr(widget, 'content', None)
    if content is not None and not callable(content):
        if isinstance(content, str):
            return content
        if hasattr(content, 'plain'):
            return str(content.plain)
        return str(content)
    label = getattr(widget, 'label', None)
    if label is not None and not callable(label):
        if hasattr(label, 'plain'):
            return str(label.plain)
        return str(label)
    r = getattr(widget, 'renderable', None)
    if r is not None and hasattr(r, 'plain'):
        return str(r.plain)
    return str(r) if r is not None else ''


def test_component_tag_requires_is_attribute():
    """Should raise a clear error during render when `:is` attribute is missing."""
    bad = import_sfc(
        """
<template>
  <VBox>
    <component id="no-is" />
  </VBox>
</template>
<script lang="py">
x = 1
</script>
""",
        raw_content=True,
    )
    vue_app = create_app(bad, backend='textual')
    vue_app.mount(run=False)
    with pytest.raises(ValueError, match=re.escape(':is')):
        vue_app.render()


def _dyn_label(screen):
    return screen.query_one('#dyn-wrap Label', Label)


def _dyn_button(screen):
    return screen.query_one('#dyn-wrap Button', Button)


def _hidden_by_display_ancestor(widget) -> bool:
    """
    Textual backend sets `display=False` on v-if containers in 
    `template_codegen`; child nodes remain in the DOM.
    """
    w = widget
    while w is not None:
        if hasattr(w, 'display'):
            try:
                if not bool(w.display):
                    return True
            except (TypeError, ValueError):
                pass
        w = getattr(w, 'parent', None)
    return False


async def test_dynamic_component_initial_is_label():
    """Renders as Label and binds `:label` when `:is` is the string `'Label'`."""
    vue_app = _create_app()
    app = vue_app.tt_app
    async with app.run_test() as pilot:
        await pilot.pause(0.2)
        w = _dyn_label(app.screen)
        assert _static_text(w) == 'dyn-line-a'


async def test_dynamic_component_switch_is_to_button():
    """
    After switching `currentView` to `'Button'`, 
    the wrapper should contain a Button.
    """
    vue_app = _create_app()
    app = vue_app.tt_app
    async with app.run_test() as pilot:
        await pilot.pause(0.2)
        _dyn_label(app.screen)

        await pilot.click('#dyn-to-button')
        await pilot.pause(0.15)
        btn = _dyn_button(app.screen)
        assert str(btn.label) == 'dyn-line-a'


async def test_dynamic_component_switch_back_to_label():
    """Toggle back and forth between Button and Label."""
    vue_app = _create_app()
    app = vue_app.tt_app
    async with app.run_test() as pilot:
        await pilot.pause(0.2)
        await pilot.click('#dyn-to-button')
        await pilot.pause(0.12)
        _dyn_button(app.screen)

        await pilot.click('#dyn-to-label')
        await pilot.pause(0.12)
        w = _dyn_label(app.screen)
        assert _static_text(w) == 'dyn-line-a'


async def test_dynamic_component_label_bind_updates_without_changing_is():
    """Updating `:label` without changing `:is` should take effect on the child component."""
    vue_app = _create_app()
    app = vue_app.tt_app
    async with app.run_test() as pilot:
        await pilot.pause(0.2)
        w = _dyn_label(app.screen)
        assert _static_text(w) == 'dyn-line-a'

        await pilot.click('#dyn-toggle-label')
        await pilot.pause(0.12)
        assert _static_text(_dyn_label(app.screen)) == 'dyn-line-b'


async def test_dynamic_component_v_if_hides():
    """
    When `v-if` is false, the subtree still exists and is hidden 
    by the wrapper container's `display` (see `VueCompCodeGen.gen` + Textual `display`).
    """
    vue_app = _create_app()
    app = vue_app.tt_app
    show = vue_app.root_component.setup_returned['show_dyn']

    async with app.run_test() as pilot:
        await pilot.pause(0.2)
        lab = _dyn_label(app.screen)
        assert not _hidden_by_display_ancestor(lab)

        show.value = False
        await pilot.pause(0.12)
        lab_hidden = _dyn_label(app.screen)
        assert list(app.screen.query('#dyn-wrap Label'))
        assert _hidden_by_display_ancestor(lab_hidden)

        show.value = True
        await pilot.pause(0.12)
        lab_shown = _dyn_label(app.screen)
        assert not _hidden_by_display_ancestor(lab_shown)
