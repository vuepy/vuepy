<template>
  <VBox id="main-container">
    <ShimmerText
      :text="text.value"
      :highlight_width="highlight_width.value"
      :interval="interval.value"
      :running="shimmer_running.value"
    />
    <VBox id="controls">
      <HBox>
        <Label label="文字:" style="width: 10;" />
        <Input v-model="text.value" placeholder="Thinking" style="width: 20;" />
      </HBox>
      <HBox>
        <Label label="高亮宽:" style="width: 10;" />
        <Input v-model="highlight_width.value" type="number" placeholder="3" style="width: 20;" />
      </HBox>
      <HBox>
        <Label label="间隔(s):" style="width: 10;" />
        <Input v-model="interval.value" type="number" placeholder="0.08" style="width: 20;" />
      </HBox>
      <HBox>
        <Button label="开始" @click="start_shimmer" />
        <Button label="停止" @click="stop_shimmer" />
      </HBox>
    </VBox>
  </VBox>
</template>

<script lang="py">
from pathlib import Path
from vuepy import ref, import_sfc

# 要显示的文字
text = ref("Thinking...")
# 高亮宽度（同时亮起的字符数），Input 绑定字符串
highlight_width = ref("3")
# 动画帧间隔（秒），Input 绑定字符串
interval = ref("0.1")
# 是否运行中
shimmer_running = ref(True)


def start_shimmer():
    if shimmer_running.value:
        return
    shimmer_running.value = True


def stop_shimmer():
    shimmer_running.value = False
</script>

<style lang="tcss">
Screen { background: rgb(40, 44, 52); }
#main-container { padding: 2; height: auto; align: center middle; }
#controls { padding: 1 0; }
#controls HBox { padding: 1 0; }
</style>
