"""Tests aligned with Vue fallthrough attrs: parent non-prop attrs reach built-in roots and props init.

参考: https://cn.vuejs.org/guide/components/attrs.html
"""
from __future__ import annotations

from pathlib import Path

from textual.widgets import Button

from vuepy import create_app, import_sfc


def _create_attrs_app():
    Root = import_sfc(Path(__file__).parent / 'test_attrs_parent.vue')
    vue_app = create_app(Root, backend='textual')
    vue_app.mount(run=False)
    return vue_app


async def test_fallthrough_id_and_click_on_builtin_button():
    """未声明为 props 的 id、@click 等应作用在内置组件根节点（类比 Vue 单根透传）。"""
    vue_app = _create_attrs_app()
    app = vue_app.tt_app
    async with app.run_test() as pilot:
        await pilot.pause(0.15)
        btn = app.screen.query_one('#fallthrough-btn', Button)
        assert btn.id == 'fallthrough-btn'


def _classes_set(widget) -> set[str]:
    c = getattr(widget, 'classes', None)
    if c is None:
        return set()
    if isinstance(c, (set, frozenset)):
        return set(c)
    return set(c) if hasattr(c, '__iter__') and not isinstance(c, str) else {str(c)}


async def test_class_attr_merged_on_builtin_button():
    """template 中的 class 会转为 Textual 的 classes（VTextualComponent._convert_class_to_classes）。"""
    vue_app = _create_attrs_app()
    app = vue_app.tt_app
    async with app.run_test() as pilot:
        await pilot.pause(0.15)
        btn = app.screen.query_one('#class-merge-btn', Button)
        names = _classes_set(btn)
        assert 'btn-base' in names
        assert 'extra-from-parent' in names


async def test_parent_non_bind_attrs_initialize_define_props():
    """父传入的 hint=\"...\" 进入子组件 ctx.attrs，与 defineProps 声明对齐时完成初始化。"""
    vue_app = _create_attrs_app()
    app = vue_app.tt_app
    attrs_child_ref = vue_app.root_component.setup_returned['attrs_child_ref']
    async with app.run_test() as pilot:
        await pilot.pause(0.15)

        attrs_child_root_widget = attrs_child_ref.value.unwrap()
        # attrs
        assert attrs_child_root_widget.id == 'attrs-child'
        assert attrs_child_root_widget.classes == {'class-from-parent'}
        # props
        assert attrs_child_ref.value.props.hint.value == 'from-parent-attrs'
