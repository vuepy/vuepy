"""RadioSet 用例：使用 vuepy + textual 后端展示单选组。

RadioSet 内可放多个 RadioButton，同一组内互斥选中。
RadioButton 的 :value="True" 表示该项为默认选中。
v-model 绑定到 RadioSet 的 value（一般为当前选中索引 pressed_index）。
"""
from vuepy import create_app, import_sfc, ref

App = import_sfc("""
<template>
<HBox>
  <Button label="set Apple" @click="set_choice(0)" />
  <Button label="set Banana" @click="set_choice(1)" />
  <Button label="set Orange" @click="set_choice(2)" />
</HBox>
<VBox style="height: 1fr; padding: 1 2;">
  <RadioSet v-model="choice.value">
    <!-- not support
    <RadioButton label="Apple" :value="True" /> 
    -->
    <RadioButton label="[red] Apple[/]" button_inner="X" />
    <RadioButton label="[yellow] Banana[/]" />
    <RadioButton :label="Text.from_markup(' :backhand_index_pointing_right:')" />
  </RadioSet>
  <Static>Selected index: {{ choice.value }}</Static>

  <RadioSet :selected_index="1">
    <RadioButton v-for="i in ('Apple', 'Banana')" :label="f'Radio {i}'" />
  </RadioSet>
</VBox>
<Footer />
</template>
<script lang="py">
from vuepy import ref
from rich.text import Text

choice = ref(-1)

def set_choice(index: int):
    choice.value = index
</script>
<style>
/* 可选：TCSS 样式 */
</style>
""", raw_content=True)

if __name__ == "__main__":
    app = create_app(App, backend="textual")
    app.mount()
