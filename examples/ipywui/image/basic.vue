<template>
  <Image v-model="img.value" format="png" style="width: 300px"></Image>
</template>

<script setup>
import Image from "../../../src/ipywui/components/Image";
</script>
<script lang="py">
from vuepy import ref

file = open("jupyter_logo.png", "rb")
img = ref(file.read())
</script>