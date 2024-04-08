<template>
<Display :obj="widget.value"></Display>
</template>

<script src="./ipywidgets_setup.py"></script>
<script setup>
import Display from "../../../src/ipywui/components/Display";
</script>