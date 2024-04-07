<template>
  <Tabs v-model="selected.value">
    <TabPane title="Tab1">
      <Slider description="slider"></Slider>
    </TabPane>

    <TabPane title="Tab2">
      <Input placeholder="input"></Input>
    </TabPane>

    <TabPane title="Tab3">
      <Button label="click" type="info"></Button>
    </TabPane>

  </Tabs>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Tabs from "../../../src/ipywui/components/Tabs";
import TabPane from "../../../src/ipywui/components/TabPane";
import Slider from "../../../src/ipywui/components/Slider";
import Input from "../../../src/ipywui/components/Input";
import Button from "../../../src/ipywui/components/Button";
</script>