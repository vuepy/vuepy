<template>
  <HBox>
    <Button @click="on_click()">Default</Button>
    <Button type="info" @click="async_click">Info</Button>
    <Button type="success">Success</Button>
    <Button type="warning">Warning</Button>
    <Button label="Danger" type="danger"></Button>
  </HBox>
  <HBox>
    <Button icon="search" @click="on_click2"></Button>
    <Button type="info" icon="edit"></Button>
    <Button type="success" icon="check"></Button>
    <Button type="warning" icon="star">{{ count.value }}</Button>
    <Button type="danger" icon="trash-alt"></Button>
  </HBox>
</template>

<script setup>
import Button from "../../../src/ipywui/components/Button";
import HBox from "../../../src/ipywui/components/HBox";
</script>
<script lang="py">
import asyncio
from vuepy import ref

count = ref(1)

def on_click():
  count.value += 1
  print("on click")

def on_click2(btn):
  print(f"{btn} on click") # Button(icon='search', style=ButtonStyle()) on click

# support async def
async def async_click(btn):
  btn.loading = True
  await asyncio.sleep(1)
  btn.loading = False
</script>