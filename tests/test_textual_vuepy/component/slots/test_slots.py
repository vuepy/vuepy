"""插槽行为测试：默认插槽、具名插槽、默认内容与简写 #header。

与 Vue 文档对应关系见: https://cn.vuejs.org/guide/components/slots.html
未覆盖：作用域插槽（v-slot=\"slotProps\"）等需编译器额外支持的能力。
"""
from __future__ import annotations

from pathlib import Path

import pytest
import textual
from textual.widgets import Label

from vuepy import create_app, import_sfc

_DIR = Path(__file__).parent


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


def _mount_parent(relative_name: str):
    Root = import_sfc(_DIR / relative_name)
    vue_app = create_app(Root, backend='textual')
    vue_app.mount(run=False)
    return vue_app.tt_app


def _label_ids_present(screen) -> set[str]:
    return {w.id for w in screen.query(Label) if getattr(w, 'id', None)}


async def test_named_and_explicit_default_slots_replace_fallbacks():
    """具名插槽 + 显式 <template v-slot:default>：父内容取代子组件 <slot> 内默认节点。"""
    app = _mount_parent('test_slots_parent_named_and_default.vue')
    async with app.run_test() as pilot:
        await pilot.pause(0.15)

        assert _static_text(app.screen.query_one('#slot-header-parent', Label)) == 'HeaderFromParent'
        assert _static_text(app.screen.query_one('#slot-default-parent', Label)) == 'DefaultFromParent'
        ids = _label_ids_present(app.screen)
        assert 'slot-header-fallback' not in ids
        assert 'slot-default-fallback' not in ids


async def test_implicit_default_slot_with_top_level_nodes():
    """顶级非 <template> 节点视为默认插槽；具名插槽仍用 <template #header>。"""
    app = _mount_parent('test_slots_parent_implicit_default.vue')
    async with app.run_test() as pilot:
        await pilot.pause(0.15)
        assert _static_text(app.screen.query_one('#slot-header-parent', Label)) == 'HeaderOnly'
        assert _static_text(app.screen.query_one('#slot-implicit-default', Label)) == 'ImplicitDefaultBody'
        ids = _label_ids_present(app.screen)
        assert 'slot-header-fallback' not in ids
        assert 'slot-default-fallback' not in ids


async def test_slot_default_content_when_parent_empty():
    """父未传入任何插槽内容时，渲染子组件 <slot> 标签之间的默认内容。"""
    app = _mount_parent('test_slots_parent_empty.vue')
    async with app.run_test() as pilot:
        await pilot.pause(0.15)
        assert _static_text(app.screen.query_one('#slot-header-fallback', Label)) == 'FB-H'
        assert _static_text(app.screen.query_one('#slot-default-fallback', Label)) == 'FB-D'
        ids = _label_ids_present(app.screen)
        assert 'slot-header-parent' not in ids
        assert 'slot-default-parent' not in ids


async def test_named_slot_only_default_slot_still_falls_back():
    """只提供 header 具名插槽时，默认插槽仍使用子组件内默认内容。"""
    app = _mount_parent('test_slots_parent_header_only.vue')
    async with app.run_test() as pilot:
        await pilot.pause(0.15)
        assert _static_text(app.screen.query_one('#slot-header-parent', Label)) == 'HeaderOnly'
        assert _static_text(app.screen.query_one('#slot-default-fallback', Label)) == 'FB-D'
        assert 'slot-default-parent' not in _label_ids_present(app.screen)


async def test_slots_render_in_correct_structure    ():
    """slot内容应按child定义顺序/slot顺序渲染。"""
    app = _mount_parent('test_slots_parent_named_and_default.vue')
    async with app.run_test() as pilot:
        await pilot.pause(0.15)
        vbox = app.screen.query_one('#slots-child-root')
        rendered_order = [
            id(w.query_one(Label)) for w in vbox.children
        ]
        child_defined_order = [
            id(app.screen.query_one('#slot-header-parent', Label)),
            id(app.screen.query_one('#not-in-slots', Label)),
            id(app.screen.query_one('#slot-default-parent', Label)),
        ]
        assert rendered_order == child_defined_order
