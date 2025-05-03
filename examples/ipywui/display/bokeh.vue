<template>
  <p>value {{ val.value }} </p>
  <Slider v-model='val.value' :min='1' :max='10' :step='1' @change='change()'/>
  <Display :obj="bo" />
</template>
<script lang='py'>
from vuepy import ref, watch
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from jupyter_bokeh.widgets import BokehModel
from bokeh.io import output_notebook

output_notebook()

val = ref(1)

x = list(range(0, 11))
source = ColumnDataSource(data={'x': x, 'y': x})
p = figure(height=300, width=600)
l = p.line(x, x, line_width=3, line_alpha=0.6)
bo = BokehModel(p)

def change():
    power = val.value
    l.data_source.data['y'] = [i**power for i in x]
    
</script>