<template>
  <HBox>
    <Button label="Default" @click="on_click()"></Button>
    <Button label="Info" type="info"></Button>
    <Button label="Success" type="success"></Button>
    <Button label="Warning" type="warning"></Button>
    <Button label="Danger" type="danger"></Button>
  </HBox>
  <HBox>
    <Button icon="search" @click="on_click2"></Button>
    <Button type="info" icon="edit"></Button>
    <Button type="success" icon="check"></Button>
    <Button type="warning" icon="star"></Button>
    <Button type="danger" icon="trash-alt"></Button>
  </HBox>
</template>

<script setup>
import Button from "../../../src/ipywui/components/Button";
import HBox from "../../../src/ipywui/components/HBox";
</script>
<script lang="py">
def on_click():
  print("on click")

def on_click2(btn):
  print(f"{btn} on click") # Button(icon='search', style=ButtonStyle()) on click
</script>