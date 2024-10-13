<template>
  <Display :obj="video"></Display>
  <p>注意：先调节音量</p>
  <Display :obj="audio"></Display>
</template>

<script setup>
import Display from "../../../src/ipywui/components/Display";
</script>
<script lang="py">
import numpy as np
from IPython.display import Video
from IPython.display import Audio

video_src = "https://github.com/vuepy/vuepy/raw/refs/heads/master/examples/ipywui/display/sora.mp4"
video = Video(video_src, width=350)

# gen sound
sr = 22050
T = 0.5
t = np.linspace(0, T, int(T * sr), endpoint=False)
x = 0.5 * np.sin(2 * np.pi * 440 * t)

audio = Audio(x, rate=sr)


</script>
