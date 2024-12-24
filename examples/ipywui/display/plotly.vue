<template>
  <Dropdown v-model="freq.value" :options="frequencies" description="Frequency"></Dropdown>
  <Slider v-model="amplitude.value" description="Amplitude"></Slider>
  <Display :obj="fig"></Display>
</template>

<script setup>
import Display from "../../../src/ipywui/components/Display";
import Dropdown from "../../../src/ipywui/components/Dropdown";
import Slider from "../../../src/ipywui/components/Slider";
</script>
<script lang="py">
import plotly.graph_objects as go
import numpy as np
from vuepy import ref, watch

frequencies = [1, 2, 3, 4]

freq = ref(frequencies[0])
amplitude = ref(1.0)

fig = go.FigureWidget()
x = np.linspace(0, 10, 400)
waves = {f: np.sin(x * f) for f in frequencies}
fig.add_trace(go.Scatter(x=x, y=waves[freq.value], name=f'Frequency {freq.value}'))


@watch([freq, amplitude])
def update_figure(new_val, _, __):
    frequency, amplitude = new_val
    fig.data[0].y = waves[frequency] * amplitude
    fig.data[0].name = f'Frequency {frequency} (Amp: {amplitude:.1f})'
    fig.update_layout(title=f'Interactive Sine Wave (Frequency: {frequency}, Amplitude: {amplitude:.1f})')

</script>
