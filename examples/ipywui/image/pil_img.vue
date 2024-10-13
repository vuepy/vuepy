<template>
  <Image :value="pil_img" style="width: 200px"></Image>
</template>

<script setup>
import Image from "../../../src/ipywui/components/Image";
</script>
<script lang="py">
from vuepy import ref
from PIL import Image

pil_img = Image.open("jupyter_logo.png")
</script>