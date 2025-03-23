<template>
  <SelectTags v-model="tags.value"
             @change="on_change"
  ></SelectTags>
  <p>basic: {{ tags.value }}</p>

  <SelectTags v-model="unique_tags.value" unique></SelectTags>
  <p>unique: {{ unique_tags.value }}</p>
</template>

<script setup>
import SelectTags from "../../../src/ipywui/components/SelectTags";
</script>
<script lang="py">
from vuepy import ref

tags = ref(['tag1', 'tag2', 'tag3'])
unique_tags = ref(['t1', 't2', 't3'])

# called when enter key is pressed or the input is blurred
def on_change(value):
    print(value) # {'new': ['tag1', 'tag2'], 'old': ['tag1', 'tag2', 'tag3'], 'owner': TagsInput(...)}
</script>
