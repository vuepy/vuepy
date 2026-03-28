<template>
<VBox>
<HBox>
    <Button label="Red" id="red" @click="switch_color('red')" />
    <Button label="Green" id="green" @click="switch_color('green')" />
    <Button label="Blue" id="blue" @click="switch_color('blue')" />
    <Button label="exit" @click="app.tt_app.exit(return_code=0)" />
</HBox>
mouse:{{ x.value }},{{ y.value }}
<Footer />
</VBox>
</template>
<script lang="py">
from vuepy import ref, onMounted
from textual_vuepy.vueuse import onKeyStroke, useMouse

def switch_color(color):
    app.tt_app.screen.styles.background = color

x, y = useMouse()

onKeyStroke('r', lambda: switch_color('red'))
onKeyStroke('g', lambda: switch_color('green'))
onKeyStroke('b', lambda: switch_color('blue'))

</script>
<style>
HBox {
    width: 1fr;
    height: 1fr;
    align: center middle;
}
</style>