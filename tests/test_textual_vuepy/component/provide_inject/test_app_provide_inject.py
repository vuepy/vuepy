"""App.provide / App.inject and TextualProvides.APP_MIXIN behavior.

See `src/textual_vuepy/_research/test.py`: `app.provide(TextualProvides.APP_MIXIN, TTAppMixin)`;
the Textual backend injects this key in `gen_document_node`, appending the mixin class to the MRO of `TextualDocRootWidget`.
"""
from __future__ import annotations

from pathlib import Path

from textual.app import App as TextualApp
from textual.widgets import Label

from vuepy import create_app, import_sfc
from vuepy.compiler_sfc.codegen_backends.textual import TextualProvides

_DIR = Path(__file__).parent


class _DemoTextualAppMixin(TextualApp):
    """
    Textual App subclass for inject testing; after multiple inheritance with 
    TextualDocRootWidget, class attributes should be accessible.
    """

    VP_PROVIDE_INJECT_TEST_MARK = 'mixin-from-provide'


def _make_vue_app():
    Root = import_sfc(_DIR / 'test_app_provide_inject_root.vue')
    return create_app(Root, backend='textual')


def test_provide_inject_arbitrary_string_key():
    """
    Arbitrary string key: after provide, 
    inject can retrieve the value; returns None when not provided.
    """
    vue_app = _make_vue_app()
    token = 'test.provide_inject.token'
    payload = {'n': 7}
    vue_app.provide(token, payload)
    assert vue_app.inject(token) is payload
    assert vue_app.inject('test.provide_inject.missing') is None


def test_provide_enum_key_inject_by_member_or_value():
    """
    Consistent with `TextualProvides`: can use either Enum member or `.value` string as key.
    """
    vue_app = _make_vue_app()
    sentinel = object()
    vue_app.provide(TextualProvides.APP_MIXIN, sentinel)
    assert vue_app.inject(TextualProvides.APP_MIXIN) is sentinel
    assert vue_app.inject(TextualProvides.APP_MIXIN.value) is None

    vue_app2 = _make_vue_app()
    vue_app2.provide(TextualProvides.APP_MIXIN.value, sentinel)
    assert vue_app2.inject(TextualProvides.APP_MIXIN.value) is sentinel
    assert vue_app2.inject(TextualProvides.APP_MIXIN) is None


def test_textual_document_root_uses_app_mixin_from_provide():
    """
    After providing `TextualProvides.APP_MIXIN`, 
    the document root before mounting should be a dynamic subclass of (mixin, TextualDocRootWidget).
    """
    vue_app = _make_vue_app()
    vue_app.provide(TextualProvides.APP_MIXIN, _DemoTextualAppMixin)
    vue_app.mount(run=False)

    tt_root = vue_app.document.unwrap()
    assert getattr(tt_root, 'VP_PROVIDE_INJECT_TEST_MARK', None) == 'mixin-from-provide'
    assert isinstance(tt_root, TextualApp)
    assert isinstance(tt_root, _DemoTextualAppMixin)


async def test_mount_app_still_renders_after_mixin_provide():
    """
    With APP_MIXIN provided, the UI should still mount normally and the root Label should be queryable.
    """
    vue_app = _make_vue_app()
    vue_app.provide(TextualProvides.APP_MIXIN, _DemoTextualAppMixin)
    vue_app.mount(run=False)
    app = vue_app.tt_app
    async with app.run_test() as pilot:
        await pilot.pause(0.12)
        w = app.screen.query_one('#provide-inject-root-label', Label)
        assert w.content == 'root'
