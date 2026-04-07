<template>
  <VBox id="key-mod-root">
    <Label id="key-mod-log" :label="key_log.value" />
    <!--
    lowercase letter: a
    uppercase letter: A
    digit: 1
    symbol: !
    function keys: f1, insert
    arrow key: up
    chord keys (modifier+)
      ctrl+(a, f1, insert, underscore, right, home)
      shift+(tab, end, up, home)
      alt+(a, up, home)
      meta(m)

      ctrl+shift+c only fires via pivot trigger
    special keys: enter, tab, escape, space, arrow_up
    -->
    <VBox
      id="kbd-capture"
      :can_focus="capture_can_focus"
      @keyup.a="mark('lower_a')"
      @keyup.shift.a="mark('A')"
      @keyup.b="mark('lower_b')"
      @keyup.1="mark('digit_1')"
      @keyup.shift.1="mark('shift_1')"
      @keyup.f1="mark('f1')"
      @keyup.insert="mark('insert')"
      @keyup.up="mark('arrow_up')"
      @keyup.right="mark('arrow_right')"
      @keyup.down="mark('arrow_down')"
      @keyup.ctrl.a="mark('ctrl_a')"
      @keyup.ctrl.f1="mark('ctrl_f1')"
      @keyup.ctrl.insert="mark('ctrl_insert')"
      @keyup.ctrl.underscore="mark('ctrl_underscore')"
      @keyup.ctrl.right="mark('ctrl_right')"
      @keyup.ctrl.home="mark('ctrl_home')"
      @keyup.shift.tab="mark('shift_tab')"
      @keyup.shift.end="mark('shift_end')"
      @keyup.shift.up="mark('shift_up')"
      @keyup.shift.home="mark('shift_home')"
      @keyup.alt.a="mark('alt_a')"
      @keyup.alt.up="mark('alt_up')"
      @keyup.alt.home="mark('alt_home')"
      @keyup.ctrl.shift.c="mark('ctrl_shift_c')"
      @keyup.meta.m="mark('meta_m')"
      @keyup.enter="mark('enter')"
      @keyup.tab="mark('tab')"
      @keyup.escape="mark('escape')"
      @keyup.space="mark('space')"
    />
  </VBox>
</template>

<script lang="py">
from vuepy import ref

key_log = ref('')
capture_can_focus = True


def mark(token):
    key_log.value = key_log.value + token + '|'
</script>

<style>
#kbd-capture {
  height: 3;
  border: solid gray;
}
</style>
