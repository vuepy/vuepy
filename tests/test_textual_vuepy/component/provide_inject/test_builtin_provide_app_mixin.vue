<template>
  <VBox>
    <Label id="builtin-app-mixin-root-label">builtin-mixin</Label>
  </VBox>
</template>

<script lang="py">
"""
Same as Keys.vue: provide APP_MIXIN in the root SFC's setup so that gen_document_node
can include it in the Textual document root.
"""
from vuepy.compiler_sfc.codegen_backends.textual import TextualProvides


class BuiltinAppMixinFromSfc:
    """Registered into the Textual document root from an SFC (same mechanism as KeyHandlerMixin in Keys.vue)."""

    MIXIN_MARK = 'builtin-from-sfc'

    def on_mount(self):
        # Textual calls both this class and TextualDocRootWidget.on_mount via MRO in order.
        # Do NOT call super() here — doing so would execute the document root callback once
        # and then trigger it a second time through MRO, causing default_body to be installed twice.
        self.builtin_mixin_on_mount_ok = True


app.provide(TextualProvides.APP_MIXIN, BuiltinAppMixinFromSfc)
</script>
