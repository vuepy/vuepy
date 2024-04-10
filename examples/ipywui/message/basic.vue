<template>
  <Button label="Show Message" type="info" @click="show_msg()"></Button>
  <Label value="" style="height: 80px"></Label>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Button from "../../../src/ipywui/components/Button";
import Label from "../../../src/ipywui/components/Label";
</script>