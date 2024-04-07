<template>
  <ToggleButtons description="Options ['pepperoni', 'pineapple', 'anchovies']"
                 v-model="choice1.value"
                 :options="options1"
  ></ToggleButtons>

  <ToggleButtons description="Options [('One', 1), ('Two', 2), ('Three', 3)]"
                 v-model="choice2.value"
                 :options="options2"
  ></ToggleButtons>

  <!--  style-->
  <ToggleButtons description="Style success"
                 type="success"
                 :options="options2"
  ></ToggleButtons>
  <ToggleButtons description="Style info"
                 type="info"
                 :options="options2"
  ></ToggleButtons>
  <ToggleButtons description="Style warning"
                 type="warning"
                 :options="options2"
  ></ToggleButtons>
  <ToggleButtons description="Style danger"
                 type="danger"
                 :options="options2"
  ></ToggleButtons>

  <!--  icon-->
  <ToggleButtons description="With icons"
                 :icons="['walking', 'car-side', 'plane']"
                 :options="['walking ', 'car ', 'plane ']"
  ></ToggleButtons>

</template>

<script src="./basic_setup.py"></script>
<script setup>
import ToggleButtons from "../../../src/ipywui/components/ToggleButtons";
</script>