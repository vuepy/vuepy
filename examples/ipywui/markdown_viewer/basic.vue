<template>
  <Input v-model="md.value" type="textarea" style="height: 150px"></Input>
  <MarkdownViewer :value="md.value"></MarkdownViewer>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Input from "../../../src/ipywui/components/Input";
import MarkdownViewer from "../../../src/ipywui/components/MarkdownViewer";
</script>