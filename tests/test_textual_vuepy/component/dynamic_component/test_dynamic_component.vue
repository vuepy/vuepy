<template>
  <VBox>
    <Button id="dyn-to-label" label="is Label" @click="set_current_view('Label')" />
    <Button id="dyn-to-button" label="is Button" @click="set_current_view('Button')" />
    <Button id="dyn-toggle-label" label="toggle label text" @click="toggle_dyn_label()" />
    <Button id="dyn-hide" label="togglehide" @click="toggle_hide()" />
    <!-- 
    id only on outer wrapper: when switching :is, new subtree mounts before old unmounts; 
    dynamic root with same id as old node triggers Textual DuplicateIds 
    -->
    <VBox id="dyn-wrap">
      <component
        :is="currentView.value"
        :label="dyn_label.value"
        v-if="show_dyn.value"
      />
    </VBox>
  </VBox>
</template>

<script lang="py">
from vuepy import ref

currentView = ref('Label')
dyn_label = ref('dyn-line-a')
show_dyn = ref(True)

def set_current_view(view):
    currentView.value = view


def toggle_hide():
    show_dyn.value = not show_dyn.value


def toggle_dyn_label():
    dyn_label.value = 'dyn-line-b' if dyn_label.value == 'dyn-line-a' else 'dyn-line-a'
</script>
