<template>
  <HBox>
    <ToggleButton label="on" :value="True" @change="on_change"></ToggleButton>
    <ToggleButton label="off" :value="False"></ToggleButton>
  </HBox>
  <HBox>
    <ToggleButton type="info" :value="True"></ToggleButton>
    <ToggleButton type="info" :value="False"></ToggleButton>
    </HBox>
  <HBox>
    <ToggleButton type="success" v-model="val1.value"></ToggleButton>
    <ToggleButton type="success" :value="False"></ToggleButton>
    </HBox>
  <HBox>
    <ToggleButton type="warning" :value="True"></ToggleButton>
    <ToggleButton type="warning"></ToggleButton>
    </HBox>
  <HBox>
    <ToggleButton type="danger" :value="True"></ToggleButton>
    <ToggleButton type="danger" :value="False"></ToggleButton>
  </HBox>
</template>

<script setup>
import ToggleButton from "../../../src/ipywui/components/ToggleButton";
import HBox from "../../../src/ipywui/components/HBox";
</script>
<script lang="py">
from vuepy import ref

val1 = ref(True)

def on_change(event):
    print(event) # {'new': False, 'old': True, 'owner': ToggleButton(...)}

</script>