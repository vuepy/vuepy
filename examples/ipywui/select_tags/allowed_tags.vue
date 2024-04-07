<template>
  <Input value="allowed_tags ['a', 'b', 'c']"></Input>
  <SelectTags
      :value="['a', 'b']"
      :allowed_tags="['a', 'b', 'c']"
  ></SelectTags>
</template>

<script setup>
import Input from "../../../src/ipywui/components/Input";
import SelectTags from "../../../src/ipywui/components/SelectTags";
</script>