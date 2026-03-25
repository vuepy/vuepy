<template>
  <VBox>
    <HBox>
      <Button label="Home" @click="go('/')" />
      <Label> | </Label>
      <Button label="About" @click="go('/about')" />
      <Label> | </Label>
      <Button label="Broken Link" @click="go('/non-existent-path')" />
    </HBox>
    <Static :content="f'当前路径: {current_path.value}'" />
    <component :is="current_view.value" />
  </VBox>
</template>

<script lang="py">
"""
Hash 风格路由的 Textual / Vuepy 对照实现。

浏览器版用 window.location.hash + hashchange；终端无 URL hash，
这里用 current_path ref + 按钮导航，路由表与 computed 解析与 Vue 一致。
"""
from pathlib import Path

from vuepy import ref, computed, import_sfc

_router_dir = Path(__file__).resolve().parent

Home = import_sfc(_router_dir / "Home.vue")
About = import_sfc(_router_dir / "About.vue")
NotFound = import_sfc(_router_dir / "NotFound.vue")

routes = {
    "/": Home,
    "/about": About,
}

# 等价于 ref(window.location.hash)：在浏览器里形如 "#/about"；这里直接存规范化路径
current_path = ref("/")


def go(path: str):
    """对应浏览器里点击 #/... 链接后 hash 变化。"""
    current_path.value = path


def _route_key(path: str) -> str:
    # 对齐 JS: currentPath.value.slice(1) || '/'
    # 若把 path 当作「去掉 # 后的部分」，空字符串视为 '/'
    p = (path or "").lstrip("#")
    return p if p else "/"


@computed
def current_view():
    key = _route_key(current_path.value)
    return routes.get(key) or NotFound
</script>
