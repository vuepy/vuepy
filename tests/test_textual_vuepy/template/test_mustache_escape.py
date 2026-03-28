"""Tests for ESCAPE_MUSTACHE_TEXT: Textual backend renders {{ }} text nodes without HTML-escaping.

ICodegenBackend.ESCAPE_MUSTACHE_TEXT = True  (default; HTML backends: ipywidgets / panel)
TextualCodegenBackend.ESCAPE_MUSTACHE_TEXT = False (terminal backend: <, >, & display literally)
"""
from __future__ import annotations

from textual.widgets import Label

from vuepy import create_app, import_sfc
from vuepy.compiler_sfc.codegen_backends.backend import ICodegenBackend
from vuepy.compiler_sfc.codegen_backends.textual import TextualCodegenBackend


def _label_text(label: Label) -> str:
    """Return the plain-text content of a Textual Label regardless of renderable type."""
    content = getattr(label, 'content', None)
    if content is None:
        content = getattr(label, 'renderable', '')
    if hasattr(content, 'plain'):
        return str(content.plain)
    return str(content)


def _build_app(ref_value: str):
    """Build a minimal Textual app with a single Label bound to a ref via mustache."""
    sfc_src = (
        "<template>\n"
        "  <VBox>\n"
        "    <Label id=\"out\">{{ val.value }}</Label>\n"
        "  </VBox>\n"
        "</template>\n"
        "<script lang=\"py\">\n"
        "from vuepy import ref\n"
        f"val = ref({ref_value!r})\n"
        "</script>\n"
    )
    Root = import_sfc(sfc_src, raw_content=True)
    vue_app = create_app(Root, backend='textual')
    vue_app.mount(run=False)
    return vue_app


# ---------------------------------------------------------------------------
# Flag tests (synchronous, no Textual app needed)
# ---------------------------------------------------------------------------

def test_textual_backend_escape_flag_is_false():
    """TextualCodegenBackend.ESCAPE_MUSTACHE_TEXT must be False."""
    assert TextualCodegenBackend.ESCAPE_MUSTACHE_TEXT is False


def test_base_backend_escape_flag_is_true():
    """ICodegenBackend.ESCAPE_MUSTACHE_TEXT must default to True for HTML backends."""
    assert ICodegenBackend.ESCAPE_MUSTACHE_TEXT is True


# ---------------------------------------------------------------------------
# Rendering tests — verify literal output in the Textual terminal backend
# ---------------------------------------------------------------------------

async def test_angle_brackets_not_escaped():
    """'<' and '>' in mustache output render literally, not as &lt;/&gt;."""
    vue_app = _build_app('x < y > z')
    async with vue_app.tt_app.run_test() as pilot:
        await pilot.pause(0.15)
        label = vue_app.tt_app.screen.query_one('#out', Label)
        assert _label_text(label) == 'x < y > z'


async def test_ampersand_not_escaped():
    """'&' in mustache output renders literally, not as &amp;."""
    vue_app = _build_app('a & b')
    async with vue_app.tt_app.run_test() as pilot:
        await pilot.pause(0.15)
        label = vue_app.tt_app.screen.query_one('#out', Label)
        assert _label_text(label) == 'a & b'


async def test_plain_text_unchanged():
    """Mustache with plain text (no special chars) renders as-is."""
    vue_app = _build_app('hello world')
    async with vue_app.tt_app.run_test() as pilot:
        await pilot.pause(0.15)
        label = vue_app.tt_app.screen.query_one('#out', Label)
        assert _label_text(label) == 'hello world'


async def test_reactive_update_not_escaped():
    """After a reactive update, '<' and '>' in the new value still render literally."""
    sfc_src = (
        "<template>\n"
        "  <VBox>\n"
        "    <Label id=\"out\">{{ val.value }}</Label>\n"
        "    <Button id=\"btn\" label=\"update\" @click=\"update()\" />\n"
        "  </VBox>\n"
        "</template>\n"
        "<script lang=\"py\">\n"
        "from vuepy import ref\n"
        "val = ref('init')\n"
        "def update():\n"
        "    val.value = 'x < y'\n"
        "</script>\n"
    )
    Root = import_sfc(sfc_src, raw_content=True)
    vue_app = create_app(Root, backend='textual')
    vue_app.mount(run=False)
    app = vue_app.tt_app

    async with app.run_test() as pilot:
        await pilot.pause(0.15)
        label = app.screen.query_one('#out', Label)
        assert _label_text(label) == 'init'

        await pilot.click('#btn')
        await pilot.pause(0.15)
        assert _label_text(label) == 'x < y'
