<template>
  <Input value="[1000, 2000, 3000] use format '$,d'"></Input>
  <SelectNumbers :value="[1000, 2000, 3000]" type="info"
                 data_type="int"
                 format="$,d"
  ></SelectNumbers>

  <Input value="[1.3, 4.56, 78.90] use format '.2f'"></Input>
  <SelectNumbers :value="[1.3, 4.56, 78.90]" type="info"
                 format=".2f"
                 tooltip="show"
  ></SelectNumbers>
</template>

<script setup>
import SelectNumbers from "../../../src/ipywui/components/SelectNumbers";
import Input from "../../../src/ipywui/components/Input";
</script>