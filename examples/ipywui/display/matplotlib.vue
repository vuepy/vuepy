<template>
  <HBox>
    <Display :obj="plt1.value"></Display>
    <Display :obj="plt2.value"></Display>
  </HBox>
  <Display :obj="plt3.value"></Display>
</template>

<script src="./matplotlib_setup.py"></script>
<script setup>
import Display from "../../../src/ipywui/components/Display";
import HBox from "../../../src/ipywui/components/HBox";
</script>