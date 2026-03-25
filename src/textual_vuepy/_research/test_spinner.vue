<template>
  <VBox id="main-container">
    <!-- TODO support class-->
    <Spinner
      :text="text.value"
      :interval="interval.value"
      :running="spinner_running.value"
      style="color: orange;"
    />
    <VBox id="controls">
      <HBox>
        <Label label="Text:" style="width: 12;" />
        <Input v-model="text.value" placeholder="Loading..." style="width: 24;" />
      </HBox>
      <HBox>
        <Label label="Interval(s):" style="width: 12;" />
        <Input v-model="interval.value" type="number" placeholder="0.1" style="width: 20;" />
      </HBox>
      <HBox>
        <Button label="Start" @click="start_spinner" />
        <Button label="Stop" @click="stop_spinner" />
      </HBox>
    </VBox>
  </VBox>
</template>

<script lang="py">
from pathlib import Path
from vuepy import ref, import_sfc

# Label text shown after the spinner character
text = ref("Loading...")
# Animation frame interval in seconds (bound as string via Input)
interval = ref("0.1")
# Whether the spinner is running
spinner_running = ref(True)


def start_spinner():
    if spinner_running.value:
        return
    spinner_running.value = True


def stop_spinner():
    spinner_running.value = False
</script>

<style lang="tcss">
Screen { background: rgb(40, 44, 52); }
#main-container { padding: 2; height: auto; align: center middle; }
#controls { padding: 1 0; }
#controls HBox { padding: 1 0; }
.spinner-label {
    color: $warning;
}
</style>
