"""Tests for v-model two-way binding: parent ref, child defineModel, and Textual Input."""
from __future__ import annotations

from pathlib import Path

from textual.widgets import Button, Input

from vuepy import create_app, import_sfc


def _create_v_model_app():
    Root = import_sfc(Path(__file__).parent / 'test_v_model_parent.vue')
    vue_app = create_app(Root, backend='textual')
    vue_app.mount(run=False)
    return vue_app


def _static_text(widget) -> str:
    """Read display text from Textual Static/Label via `.content`; older wrappers may use `.label` or `renderable`."""
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


async def test_update_from_parent_to_child():
    """Parent ref changes propagate through v-model; child Label and Input match the parent value."""
    vue_app = _create_v_model_app()
    app = vue_app.tt_app
    msg_ref = vue_app.root_component.setup_returned['msg']
    async with app.run_test() as pilot:
        await pilot.pause(0.15)
        msg_label = app.screen.query_one('#msg-display')
        child_inp = app.screen.query_one('#v-model-input', Input)
        assert _static_text(msg_label) == 'Hello World!'

        msg_ref.value = 'from parent'
        await pilot.pause(0.08)
        assert _static_text(msg_label) == 'from parent'
        assert child_inp.value == 'from parent'

        msg_ref.value = ''
        await pilot.pause(0.08)
        assert _static_text(msg_label) == ''
        assert child_inp.value == ''


async def test_update_from_child_input_to_parent():
    """Typing in the child Input syncs to the parent ref via v-model; Label matches Input."""
    vue_app = _create_v_model_app()
    app = vue_app.tt_app
    async with app.run_test() as pilot:
        msg_ref = vue_app.root_component.setup_returned['msg']

        await pilot.pause(0.15)
        msg_label = app.screen.query_one('#msg-display')
        assert _static_text(msg_label) == 'Hello World!'

        child_input = app.screen.query_one('#v-model-input', Input)
        await pilot.click(child_input)
        input_text = 'input from child'
        await pilot.press(*input_text)
        await pilot.pause(0.08)

        assert child_input.value == input_text
        assert msg_ref.value == input_text
        assert _static_text(msg_label) == input_text


async def test_update_from_child_set_value_to_parent():
    """Clicking the child Button updates the model via v-model; parent ref and Label match."""
    vue_app = _create_v_model_app()
    app = vue_app.tt_app
    async with app.run_test() as pilot:
        btn_value_ref = vue_app.root_component.setup_returned['btn_value']
        child_ref = vue_app.root_component.setup_returned['child_ref']

        await pilot.pause(0.15)
        btn_label = app.screen.query_one('#btn-value-display')
        assert _static_text(btn_label) == ''

        child_btn = app.screen.query_one('#btn', Button)
        await pilot.click(child_btn)
        await pilot.pause(0.08)
        expected_btn_value = 'x'

        assert child_ref.value.model_btn.value == expected_btn_value
        assert btn_value_ref.value == expected_btn_value
        assert _static_text(btn_label) == expected_btn_value
