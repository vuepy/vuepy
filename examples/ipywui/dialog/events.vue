<template>
  <Button label="show dialog" type='info' @click="show()"></Button>
  <Label :value="state.value" style="height: 200px"></Label>
  <Dialog title="Shipping address" v-model="is_show.value" width="55%"
          @close="handle_close()"
          @open="handle_open()"
  >
    <template>
      <Input placeholder="name"></Input>
    </template>
    <template v-slot:footer>
      <HBox>
        <Button label="Cancel" type="warning" @click="close()"></Button>
        <Button label="Ok" type="info" @click="close()"></Button>
      </HBox>
    </template>
  </Dialog>
</template>

<script src="./events_setup.py"></script>
<script setup>
import Dialog from "../../../src/ipywui/components/Dialog";
import Button from "../../../src/ipywui/components/Button";
import Label from "../../../src/ipywui/components/Label";
import Input from "../../../src/ipywui/components/Input";
import HBox from "../../../src/ipywui/components/HBox";
</script>