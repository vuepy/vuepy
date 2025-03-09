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
    <span>a progressive, incrementally-adoptable Python framework <br>for building UI on the Jupyter Notebook.</span>
      <br>
      <a href="#installation">installation</a> .
      <a href="https://www.vuepy.org/guide/introduction.html">docs</a> .
      <!--<a href="">discord</a> .-->
      <a href="https://www.vuepy.org/guide/quick-start.html">learn</a>
  </p>
</samp>

## About

Vue.py (pronounced /vjuːpaɪ/, like "view py") is a Python framework for building user interfaces. It is built upon standard HTML, CSS, and Python, offering a declarative and component-based programming model that aids in the efficient development of user interfaces. Vue.py is capable of handling both simple and complex interfaces.

* 🛠️ create custom Jupyter UI using pure Python
* 🤖 prototype within .ipynb or .py files
* 🪄 reactive: update the data, vuepy will reactively update all dependent view components
* 🚀 batteries-included: built-in IPywUI includes 37+ commonly used UI components
* 🧩 extensible: can easily integrate third-party libraries such as plotly, pandas, etc
* 🖐️ interactive: bind sliders, buttons, plots, and more to Python — no callbacks required
* 🚀 run in Jupyter, JupyterLab, VSCode, Cursor, Google Colab and more
* ✨ generate UI interface with one click through AI-driven conversation interface. provide [llms.txt](https://www.vuepy.org/llms.txt), [llms-ctx.txt](https://www.vuepy.org/llms-ctx.txt), []()

## Installation

**Vue.py** is available on [PyPI](https://pypi.org/project/org.vuepy.core/):

```bash
pip install "org.vuepy.core"
```

## Usage

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

Read [the documentation](https://www.vuepy.org/guide/quick-start.html) to learn more.

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