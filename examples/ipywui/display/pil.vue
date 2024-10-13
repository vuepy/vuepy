<template>
  <Display :obj="pil_img"></Display>
</template>

<script setup>
import Display from "../../../src/ipywui/components/Display";
</script>
<script lang="py">
from PIL import Image

pil_img = Image.open("jupyter_logo.jpg")

</script>