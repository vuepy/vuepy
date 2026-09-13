<h1>
  <p align="center" style="color: #16b8f3">
    <img width="180" src="https://github.com/vuepy/vuepy/blob/master/docs/assets/vuepy-logo.svg?raw=true">
    <!--
    <img src="./docs/assets/vuepy-logo.svg" width="180">
    <img src="https://github.com/vuepy/vuepy/blob/master/docs/assets/vuepy-logo.svg?raw=true"
         alt="vue.py logo." width="120" style="vertical-align: middle"
    >Vue.py
    -->
  </p>
</h1>
<samp>
  <p align="center">
    <span>a progressive, incrementally-adoptable Python framework <br>for building <b>Jupyter web interfaces</b> &amp; <b>terminal TUI apps</b>.</span>
      <br>
      <a href="#installation">installation</a> .
      <a href="https://www.vuepy.org/guide/introduction.html">docs</a> .
      <!--<a href="">discord</a> .-->
      <a href="https://www.vuepy.org/guide/quick-start.html">learn</a> .
      <a href="https://www.vuepy.org/textual_vuepy/quick-start.html">TUI</a>
  </p>
</samp>

## About

Vue.py (pronounced /vjuːpaɪ/, like "view py") is a reactive Python framework for building **Jupyter web interfaces** and **terminal TUI applications**. Built upon standard HTML, CSS, and Python, it offers a declarative and component-based programming model — the same `.vue` SFC syntax works across all backends.

* 🛠️ create custom web interfaces using pure Python in Jupyter
* 🖥️ build terminal TUI apps with [Textual-vuepy](https://www.vuepy.org/textual_vuepy/quick-start.html) — run anywhere, deploy via web with `textual-serve`
* 🤖 prototype within `.ipynb` or `.py` files, or run directly with `vuepy run App.vue`
* 🪄 reactive: update the data, vuepy will reactively update all dependent view components
* 🚀 batteries-included: built-in [IPywUI](https://vuepy.org/ipywui/overview.html) includes 37+ commonly used UI components
* 🚀 batteries-included: [Panel-vuepy](https://vuepy.org/panel_vuepy/quick-start.html) includes 130+ commonly used UI components
* 🚀️ batteries-included: [Textual-vuepy](https://vuepy.org/textual_vuepy/quick-start.html) wraps all Textual widgets as Vue components for terminal TUI
* 🧩 extensible: easily integrate third-party libraries such as plotly, bokeh, panel, pandas, ipyleaflet, etc.
* 🖐️ interactive: bind sliders, buttons, plots, and more to Python — no callbacks required
* 🚀 run in Jupyter, JupyterLab, VSCode, Cursor, Google Colab, terminal and more
* ✨ generate UI interface with one click through AI. provides [llms.txt](https://www.vuepy.org/llms.txt), [llms-ctx.txt](https://www.vuepy.org/llms-ctx.txt)

## Installation

**Vue.py** is available on [PyPI](https://pypi.org/project/vuepy-core/):

```bash
# Jupyter web interface (default)
pip install vuepy-core[all]

# Terminal TUI apps (includes Textual-vuepy)
pip install 'vuepy-core[textual]'
```

## Usage

### Jupyter Web Interface

```python
from vuepy import ref, create_app

def setup(*args):
    count = ref(0)
    
    def counter():
        count.value += 1
    
    return locals()

app = create_app({
    'setup': setup,
    'template': '''
    <Button :label="f'Count is: {count.value}'" 
      @click='counter()'
    ></Button>
    '''
})
app.mount()
```

![](https://github.com/vuepy/vuepy/blob/master/docs/assets/readme-demo.gif?raw=true)

### Terminal TUI App

Write a `.vue` SFC file and run it directly from the command line:

```vue
<!-- App.vue -->
<template>
  <VBox style="height: 1fr; align: center middle;">
    <Label :label="f'Count: {count.value}'" />
    <HBox>
      <Button label="+" @click="increment()" />
      <Button label="-" @click="decrement()" />
    </HBox>
  </VBox>
</template>

<script lang="py">
from vuepy import ref

count = ref(0)

def increment():
    count.value += 1

def decrement():
    count.value -= 1
</script>
```

```bash
vuepy run App.vue
```

Read [the documentation](https://www.vuepy.org/guide/quick-start.html) to learn more, or check out [Textual-vuepy docs](https://www.vuepy.org/textual_vuepy/quick-start.html) for terminal TUI apps.

## Learn more

vuepy is easy to get started with, with lots of room for powers users.

Check out our [docs](https://www.vuepy.org/guide/introduction.html), the `examples/` folder, and our gallery to learn more.

<table>
  <tr>
    <th></th> <th>Desc</th> <th>Link</th>
  </tr>
  <tr>
    <td><img src="https://github.com/vuepy/vuepy/blob/master/docs/assets/readme-demo.gif?raw=true" with='389px'></td>
    <td>Reactivity</td>
    <td><a target="_blank" href="https://www.vuepy.org/guide/essentials/reactivity-fundamentals.html">Read more</a> </td>
  </tr>
  <tr>
    <td><img src='https://github.com/vuepy/vuepy/blob/master/docs/assets/plotly.gif?raw=true' with='389px'></td>
    <td>Interacting with <a target="_blank" href="https://plotly.com/python/">plotly</a></td>
    <td><a target="_blank" href="https://www.vuepy.org/ipywui/display.html#%E9%9B%86%E6%88%90-plotly-%E7%BB%98%E5%9B%BE%E7%BB%84%E4%BB%B6">Read more</a> </td>
  </tr>
  <tr>
    <td><img src='https://github.com/vuepy/vuepy/blob/master/docs/assets/run-in-vscode.gif?raw=true' with='389px'></td>
    <td>Run in VSCode</td>
    <td><a target="_blank" href="https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter">Read more</a> </td>
  </tr>
  <tr>
    <td><img src='https://github.com/vuepy/vuepy/blob/master/docs/assets/cursor_10fps.gif?raw=true' with='389px'></td>
    <td>Building vuepy app with LLMs</td>
    <td><a target="_blank" href="https://www.vuepy.org/guide/build-vuepy-withs-llms.html">Read more</a> </td>
  </tr>
  <tr>
    <td><img src='https://github.com/vuepy/vuepy/blob/master/docs/assets/vleaflet-demo-orgin-low.gif?raw=true' with='389px'></td>
    <td>vleaflet interactive maps demo</td>
    <td>
      <a target="_blank" href="https://github.com/vuepy/vuepy/blob/master/examples/vleaflet_travel/travel.ipynb">Read more</a>, 
      <a target="_blank" href="https://www.vuepy.org/vleaflet/overview.html">docs</a>
    </td>
  </tr>
  <tr>
    <td>🖥️ Terminal TUI</td>
    <td>Textual-vuepy: build terminal TUI apps with the same .vue syntax, run via <code>vuepy run App.vue</code></td>
    <td><a target="_blank" href="https://www.vuepy.org/textual_vuepy/quick-start.html">docs</a></td>
  </tr>
  <!--
  <tr>
    <td><img src='https://github.com/vuepy/vuepy/blob/master/docs/assets/vleaflet-demo-orgin-low.gif?raw=true' with='389px'></td>
    <td>Panel-vuepy</td>
    <td>
      <a target="_blank" href="https://github.com/vuepy/vuepy/blob/master/examples/vleaflet_travel/travel.ipynb">Read more</a>, 
      <a target="_blank" href="https://www.vuepy.org/panel_vuepy/quick-start.html">docs</a>
    </td>
  </tr>
  -->
</table>


## Support

Having trouble? Get help in our [Discord](https://discord.gg/) or open
a [Discussion](https://github.com/vuepy/vuepy/issues/new).

## Contributing

**New contributors welcome!** 
<!--Check out our
[Contributors Guide](./CONTRIBUTING.md) for help getting started.

Join us on [Discord](https://discord.gg/) to meet other maintainers.
We'll help you get your first contribution in no time!
-->

<!--
## Citation

If you use **vuepy** in your work, please consider citing the following
publications:

Our [JOSS paper](https://joss.theoj.org/papers/10.21105/joss.06939) describing
the overall project and vision:

```bibtex
@article{manz2024anywidget,
  title = {anywidget: reusable widgets for interactive analysis and visualization in computational notebooks},
  volume = {9},
  url = {https://doi.org/10.21105/joss.06939},
  doi = {10.21105/joss.06939},
  number = {102},
  journal = {Journal of Open Source Software},
  author = {Manz, Trevor and Abdennur, Nezar and Gehlenborg, Nils},
  year = {2024},
  note = {Publisher: The Open Journal},
  pages = {6939},
}
```

Our [SciPy paper](https://proceedings.scipy.org/articles/NRPV2311), detailing
the motivation and approach behind Jupyter Widget ecosystem compatability:

```bibtex
@inproceedings{manz2024notebooks,
  title = {Any notebook served: authoring and sharing reusable interactive widgets},
  copyright = {https://creativecommons.org/licenses/by/4.0/},
  url = {https://doi.curvenote.com/10.25080/NRPV2311},
  doi = {10.25080/NRPV2311},
  urldate = {2024-10-07},
  booktitle = {Proceedings of the 23rd {Python} in {Science} {Conference}},
  author = {Manz, Trevor and Gehlenborg, Nils and Abdennur, Nezar},
  month = jul,
  year = {2024},
}
```
-->

## License

[MIT](https://github.com/vuepy/vuepy/blob/master/LICENSE)