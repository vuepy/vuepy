<template>
  <Button label="Compile in sub component"
          @click="submit()"
          button_style="info"
  ></Button>
  <Input v-model="model.value" placeholder="compile input"></Input>
  <pre>
    v-model: {{ model.value }}
    text: `{{ text.value }}`
    props dynamic: `{{ props.dynamic.value }}`
    props static: `{{ props.static.value }}`
  </pre>
</template>

<script src="./Compile_setup.py"></script>
<script setup>
import Button from "../../src/ipywui/components/Button";
import Input from "../../src/ipywui/components/Input";
</script>

<style scoped>

</style>