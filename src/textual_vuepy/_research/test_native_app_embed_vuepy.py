"""
原生 Textual App + 中间区域由 vuepy SFC 渲染。

用法（需在 py3.10 且已安装 textual / vuepy）::

    python -m textual_vuepy._research.test_native_app_embed_vuepy

要点：不要用 vp_app.mount()（那会跑 vuepy 自带的 TextualDocRootWidget 子类 App）；
先 create_app(..., backend=\"textual\")，再 render()，把 vp_app.dom.unwrap()
挂到你自己的 compose 里的容器上。
"""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Footer, Static

from vuepy import create_app, import_sfc

# 仅作为「嵌入的子树」；根节点用 VBox 与现有示例一致
VueCounter = import_sfc(
    """
<template>
  <VBox id="vuepy-counter-root">
    <Static> 计数（vuepy）: {{ n.value }}</Static>
    <HBox>
      <Button label=" +1 " @click="inc" />
      <Button label=" -1 " @click="dec" />
      <Button label=" 重置 " @click="reset" />
    </HBox>
  </VBox>
</template>
<script lang="py">
from vuepy import ref

n = ref(0)

def inc():
    n.value += 1

def dec():
    n.value -= 1

def reset():
    n.value = 0
</script>
<style>
VBox#vuepy-counter-root {
    height: auto;
    padding: 1 2;
}
Static {
    margin-bottom: 1;
}
</style>
""",
    raw_content=True,
)


class NativeShellApp(App):
    """外层完全是 Textual；中间 #vuepy_host 里的子树来自 vuepy。"""

    CSS = """
    Screen {
        layout: vertical;
    }
    #banner {
        height: 3;
        padding: 1 2;
        background: $surface;
        color: $text;
    }
    #vuepy_host {
        height: 1fr;
        border: tall $accent;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static(
            "这是原生 Textual 的 Static（banner）。下方边框内为 vuepy 渲染的组件。",
            id="banner",
        )
        yield Container(id="vuepy_host")
        yield Footer()

    def on_mount(self) -> None:
        self._vp_app = create_app(VueCounter, backend="textual")
        self._vp_app.render()
        host = self.query_one("#vuepy_host")
        host.mount(self._vp_app.dom.unwrap())


if __name__ == "__main__":
    NativeShellApp().run()
