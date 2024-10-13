<template>
  <Display :obj="df1"></Display>
  <Display :obj="df2"></Display>
</template>

<script setup>
import Display from "../../../src/ipywui/components/Display";
</script>
<script lang="py">
import pandas as pd

df1 = pd.DataFrame(data={
    'col1': [1, 2],
    'col2': [3, 4],
    'col3': [5, 6],
})

df2 = pd.DataFrame(data={
    'col1': ['a', 'b'],
    'col2': ['c', 'd'],
    'col3': ['e', 'f'],
})

</script>
