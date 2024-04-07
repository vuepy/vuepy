<template>
  <HBox>
    <Text v-model="copytext.value"></Text>
    <Clipboard :copy="copytext.value">
      <Button desc="copy" type="info"></Button>
    </Clipboard>
  </HBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Clipboard from "../../../src/ipywui/components/Clipboard";
import Button from "../../../src/ipywui/components/Button";
import Text from "../../../src/ipywui/components/Text";
import HBox from "../../../src/ipywui/components/HBox";
</script>