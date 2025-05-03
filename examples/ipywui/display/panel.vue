<template>
  <p>ref value {{ a.value }} </p>
  <Display :obj="pn_slider" />
  <Display :obj="pn_row" />
</template>
<script lang='py'>
from vuepy import ref
import panel as pn

pn.extension()

a = ref(5)
pn_slider = pn.widgets.FloatSlider(name='Panel Slider', start=0, end=10, value=5)
pn_slider.param.watch(lambda ev: setattr(a, 'value', ev.new), 'value')
# pn.bind(lambda val: setattr(a, 'value', val), pn_slider, watch=True)

x = pn.widgets.Select(name='x', options=['a', 'b', 'c'])
y = pn.widgets.Select(name='y', options=[1, 2, 3])
pn_row = pn.Row(x, y)
</script>