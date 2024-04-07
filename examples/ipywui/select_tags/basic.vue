<template>
  <SelectTags v-model="tags.value"></SelectTags>
  <Input label='basic' :value="str(tags.value)"></Input>

  <SelectTags v-model="unique_tags.value" unique></SelectTags>
  <Input label='unique' :value="str(unique_tags.value)"></Input>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import SelectTags from "../../../src/ipywui/components/SelectTags";
import Input from "../../../src/ipywui/components/Input";
</script>