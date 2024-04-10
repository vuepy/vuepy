<template>
  <HBox>
    <Input v-model="copytext.value"></Input>
    <Clipboard :copy="copytext.value">
      <Button label="copy" type="info"></Button>
    </Clipboard>
  </HBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Clipboard from "../../../src/ipywui/components/Clipboard";
import Button from "../../../src/ipywui/components/Button";
import HBox from "../../../src/ipywui/components/HBox";
import Input from "../../../src/ipywui/components/Input";
</script>