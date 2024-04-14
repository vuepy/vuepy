<template>
  <HBox>
    <Input v-model="md.value" type="textarea" style="height: 150px"></Input>
    <MarkdownViewer :value="md.value"></MarkdownViewer>
  </HBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Input from "../../../src/ipywui/components/Input";
import MarkdownViewer from "../../../src/ipywui/components/MarkdownViewer";
import HBox from "../../../src/ipywui/components/HBox";
</script>