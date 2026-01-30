"""OptionList 用例：使用 vuepy + Textual 后端展示可选列表。

OptionList 内可放多个 Option，用方向键/Enter 选择。
- v-model 绑定 selected（Enter 确认的选项索引，int | None）。
- v-model:highlighted 绑定当前高亮索引（int | None）。
- @option_list_option_selected 监听选中事件（Enter 确认时）。
"""
from vuepy import create_app, import_sfc, ref

App = import_sfc("""
<template>
<VBox>
  <HBox style="padding: 1 2;">
    <Button label="set 0" @click="set_selected(0)" />
    <Button label="set 2" @click="set_selected(2)" />
    <Button label="set 5" @click="set_selected(3)" />
  </HBox>
  <VBox style="height: 1fr; padding: 1 2;">
    <!--
      v-model:highlighted="highlighted_index.value"
      @option_list_option_selected="on_option_selected"
    -->
    <OptionList
      v-model="selected_index.value"
      v-model:highlighted="highlighted_index.value"
      style="height: auto;"
    >
      <Option prompt="Aerilon" id="aer" />
      <Option prompt="Canceron" id="can" />
      <Option prompt="Caprica（禁用）" id="cap" :disabled="True" />
      <Option prompt="Virgon" id="vir" />
    </OptionList>
    <Static style="padding: 1 0;">
      v-model（selected，Enter 确认的索引）: {{ selected_index.value }}
    </Static>
    <Static style="padding: 1 0;">
      v-model:highlighted（当前高亮索引）: {{ highlighted_index.value }}
    </Static>
    <Static style="padding: 1 0;">
      已选详情: {{ selected_text.value }}
    </Static>
    <Static style="padding: 0 0 1 0;">
      方向键移动，Enter 确认；按钮可外部设置高亮
    </Static>
  </VBox>
  <Footer />
</VBox>
</template>
<script lang="py">
from vuepy import ref

selected_index = ref(None)
highlighted_index = ref(None)
selected_text = ref("（未选择）")

def set_highlight(index: int):
    highlighted_index.value = index

def set_selected(index: int):
    selected_index.value = index

def on_option_selected(event):
    opt_id = getattr(event, "option_id", None)
    idx = getattr(event, "option_index", getattr(event, "index", -1))
    prompt = getattr(getattr(event, "option", None), "prompt", "") or ""
    selected_index.value = idx  # 显式更新，与 v-model 同步
    selected_text.value = f"id={opt_id}, index={idx}, prompt={prompt}"
</script>
""", raw_content=True)

if __name__ == "__main__":
    app = create_app(App, backend="textual")
    app.mount()
