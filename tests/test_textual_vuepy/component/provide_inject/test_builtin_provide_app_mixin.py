"""Regression tests for `app.provide(TextualProvides.APP_MIXIN, ...)` in the root SFC
(consistent with Keys.vue).

`gen_document_node` calls `inject(APP_MIXIN)` on the first access to `App.document`,
placing the mixin before `TextualDocRootWidget` to compose the document root type;
provide occurs during the `SFC.gen()` / `create_app` phase, before the lazy creation
of `document`.
"""
from __future__ import annotations

from pathlib import Path

import pytest
from textual.app import App as TextualApp
from textual.widgets import Label

from vuepy import create_app, import_sfc
from vuepy.compiler_sfc.codegen_backends.textual import TextualProvides

_DIR = Path(__file__).parent


def _make_vue_app():
    Root = import_sfc(_DIR / 'test_builtin_provide_app_mixin.vue')
    return create_app(Root, backend='textual')


def test_sfc_setup_provide_app_mixin_visible_to_inject():
    vue_app = _make_vue_app()
    cls = vue_app.inject(TextualProvides.APP_MIXIN)
    assert cls is not None
    assert cls.__name__ == 'BuiltinAppMixinFromSfc'
    assert getattr(cls, 'MIXIN_MARK', None) == 'builtin-from-sfc'


def test_document_root_dynamic_subclass_includes_sfc_mixin():
    vue_app = _make_vue_app()
    mixin_cls = vue_app.inject(TextualProvides.APP_MIXIN)
    vue_app.mount(run=False)

    tt_root = vue_app.document.unwrap()
    assert getattr(tt_root, 'MIXIN_MARK', None) == 'builtin-from-sfc'
    assert getattr(tt_root, 'builtin_mixin_on_mount_ok', False) is False
    assert isinstance(tt_root, TextualApp)
    assert isinstance(tt_root, mixin_cls)


@pytest.mark.asyncio
async def test_mount_ui_and_mixin_on_mount_chain():
    """After full mount the UI is queryable and the mixin's on_mount has been called by Textual
    (see comment in .vue — do not call super() on the document root)."""
    vue_app = _make_vue_app()
    vue_app.mount(run=False)
    app = vue_app.tt_app
    async with app.run_test() as pilot:
        await pilot.pause(0.12)
        w = app.screen.query_one('#builtin-app-mixin-root-label', Label)
        assert w.content == 'builtin-mixin'
        assert getattr(app, 'builtin_mixin_on_mount_ok', False) is True
