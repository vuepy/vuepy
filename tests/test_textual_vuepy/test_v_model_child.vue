<script lang="py">
from vuepy import defineModel
model = defineModel('value')
model_btn = defineModel('btn_value', '')

def update():
    model_btn.value += 'x'
</script>

<template>
  <Label>My input</Label> 
  <Input id="v-model-input" v-model="model.value" style="width: 20;"/>
  <Label>My btn_value {{ model_btn.value }}</Label> 
  <Button id="btn" label="btn_value" @click="update" />
</template>