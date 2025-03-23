<template>
  <Accordion v-model="selected.value" @change="on_change">
    <AccordionItem title="Item0">
      <Slider description="slider"></Slider>
    </AccordionItem>

    <AccordionItem title="Item1">
      <Input placeholder="input"></Input>
    </AccordionItem>

    <AccordionItem title="Item2">
      <Button label="click" type="info"></Button>
    </AccordionItem>

  </Accordion>
</template>
<script setup>
import Accordion from "../../../src/ipywui/components/Accordion";
import AccordionItem from "../../../src/ipywui/components/AccordionItem";
import Slider from "../../../src/ipywui/components/Slider";
import Input from "../../../src/ipywui/components/Input";
import Button from "../../../src/ipywui/components/Button";
</script>
<script lang="py">
from vuepy import ref

selected = ref(1)

def on_change(event):
    print(event) # {'new': 1, 'old': 0, 'owner': Accordion(...)}
</script>