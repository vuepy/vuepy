<template>
  <Button label="show" type="info" @click="show()"></Button>
  <Label value="" style="height: 80px"></Label>
</template>

<script src="./closeable_setup.py"></script>
<script setup>
import Button from "../../../src/ipywui/components/Button";
import Label from "../../../src/ipywui/components/Label";
</script>