<template>
<VBox id="keys-root" style="height: 1fr;">
  <RichLog
    ref="key_log"
    id="keys-log"
    style="height: 1fr;"
    highlight
  />
  <HBox id="keys-footer">
    <Button id="btn-clear" label="Clear" @click="clear_log()" />
    <Button id="btn-quit" label="Quit" @click="quit_app()" />
  </HBox>
</VBox>
</template>

<script lang="py">
"""
keys app
"""
from vuepy import onMounted, ref
from vuepy.compiler_sfc.codegen_backends.textual import TextualProvides

key_log = ref(None)


def clear_log():
    node = key_log.value
    if node is None:
        return
    rl = node.unwrap()
    rl.clear()
    rl.focus()


def quit_app():
    app.tt_app.exit(return_code=0)


@onMounted
def _focus_log():
    node = key_log.value
    if node is None:
        return
    rl = node.unwrap()
    rl.focus()


class KeyHandlerMixin:
    def _on_key(self, event) -> None:
        key_log.value.unwrap().write(repr(event))

app.provide(TextualProvides.APP_MIXIN, KeyHandlerMixin)

</script>

<style lang="tcss">
Screen {
    background: #1a1d23;
}

#keys-root {
    height: 1fr;
}

#keys-log {
    height: 1fr;
    background: #1e1e1e;
    border: solid #3d3d3d;
    padding: 0 1;
}

#keys-footer {
    height: 3;
    layout: horizontal;
    margin-top: 1;
}

#btn-clear {
    width: 1fr;
    background: #e8943c;
    color: #0d0d0d;
    text-style: bold;
}

#btn-quit {
    width: 1fr;
    background: #a83850;
    color: #f5f5f5;
    text-style: bold;
}
</style>
