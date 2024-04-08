<template>
  <Display :obj="df1.value"></Display>
  <Display :obj="df2.value"></Display>
</template>

<script src="./pandas_df_setup.py"></script>
<script setup>
import Display from "../../../src/ipywui/components/Display";
</script>