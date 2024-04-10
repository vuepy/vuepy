<template>
  <Button label="Success" type="info" @click="show_success()"></Button>
  <Button label="Info" type="info" @click="show_info()"></Button>
  <Button label="Warning" type="info" @click="show_warning()"></Button>
  <Button label="Error" type="info" @click="show_error()"></Button>
  <Label value="" style="height: 80px"></Label>
</template>

<script src="./different_types_setup.py"></script>
<script setup>
import Button from "../../../src/ipywui/components/Button";
import Label from "../../../src/ipywui/components/Label";
</script>