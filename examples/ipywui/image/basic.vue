<template>
  <Image v-model="img.value" format="png" style="width: 200px"></Image>

  <Image
      v-model="img.value" format="png"
      style="width: 200px; border: 2px solid deepskyblue"
  ></Image>

  <Image
      v-model="img.value" format="png"
      :style="'width: 200px; border: 2px solid {}'.format('blue')"
  ></Image>
</template>

<script setup>
import Image from "../../../src/ipywui/components/Image";
</script>
<script lang="py">
from vuepy import ref

file = open("jupyter_logo.png", "rb")
img = ref(file.read())
</script>