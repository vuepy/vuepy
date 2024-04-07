<template>
  <Accordion v-model="selected.value">
    <AccordionItem title="Item1">
      <Slider description="slider"></Slider>
    </AccordionItem>

    <AccordionItem title="Item2">
      <Input placeholder="input"></Input>
    </AccordionItem>

    <AccordionItem title="Item3">
      <Button label="click" type="info"></Button>
    </AccordionItem>

  </Accordion>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Accordion from "../../../src/ipywui/components/Accordion";
import AccordionItem from "../../../src/ipywui/components/AccordionItem";
import Slider from "../../../src/ipywui/components/Slider";
import Input from "../../../src/ipywui/components/Input";
import Button from "../../../src/ipywui/components/Button";
</script>