<template>
  <SelectNumbers v-model="nums.value"
                 @change="on_change"
  ></SelectNumbers>
  <p>float nums: {{ nums.value }}</p>

  <SelectNumbers v-model="int_nums.value"
                 data_type="int"
  ></SelectNumbers>
  <p>int nums: {{ int_nums.value }}</p>
</template>
<script setup>
import SelectNumbers from "../../../src/ipywui/components/SelectNumbers";
</script>
<script lang="py">
from vuepy import ref

nums = ref([1, 2, 3])
int_nums = ref([1, 2, 3])

# called when enter key is pressed or the input is blurred
def on_change(value):
    print(value) # {'new': [1, 2], 'old': [1, 2, 3], 'owner': FloatsInput(...)}

</script>
