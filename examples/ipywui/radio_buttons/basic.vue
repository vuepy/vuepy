<template>
  <RadioButtons description="Options ['pepperoni', 'pineapple', 'anchovies']"
                v-model="choice1.value"
                :options="options1"
  ></RadioButtons>

  <RadioButtons description="Options [('One', 1), ('Two', 2), ('Three', 3)]"
                v-model="choice2.value"
                :options="options2"
  ></RadioButtons>

</template>

<script src="./basic_setup.py"></script>
<script setup>
import RadioButtons from "../../../src/ipywui/components/RadioButtons";
</script>