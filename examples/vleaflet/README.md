<h1>
  <p align="center" style="color: #008c8c">
    <img width="40" src="https://www.vuepy.org/images/vleaflet-logo.svg">vLeaflet
  </p>
</h1>


[vleaflet](https://www.vuepy.org/vleaflet/overview.html) is a responsive map component library built on top of [Vue.py](https://github.com/vuepy/vuepy) and [ipyleaflet](https://ipyleaflet.readthedocs.io/en/latest/index.html). It allows you to create interactive maps within Jupyter notebooks, where every object (including maps, TileLayers, layers, controls, etc.) is reactive. You can dynamically update properties from Python or the browser.

![](https://www.vuepy.org/images/vleaflet-demo-orgin-low.gif)

## Features

- Responsive and interactive maps
- Built on Vue.py and ipyleaflet
- Easy integration with Jupyter notebooks
- Reactive components for dynamic updates
- Leverages Vue.py's ecosystem for building interactive applications.

## Installation

To install vleaflet, you can use pip:

```sh
pip install 'vuepy-core[vleaflet]'
```

## Quick Start

To get started with vleaflet, please refer to the [Quick Start Guide](docs/vue-docs-zh-cn/src/vleaflet/quick-start.md) for installation steps, prerequisites, and example code snippets.

### Usage

You can use vleaflet in different ways depending on your workflow:

Using the `use` Plugin Method

```python
from vuepy import create_app, import_sfc
from vleaflet import leaflet

App = import_sfc('App.vue')  # Update with the actual path to App.vue
app = create_app(App)
app.use(leaflet)
app.mount()
```

Using `%vuepy_run`

```python
from vuepy.utils import magic
from vleaflet import leaflet

%vuepy_run app.vue --plugins leaflet
```

Using `%%vuepy_run`

```python
from vuepy.utils import magic
from vleaflet import leaflet

# -- cell --
%%vuepy_run --plugins leaflet
<template>
  <vl-map :center="[53, 354]" />
</template>
```

## Documentation

For more detailed information about the vleaflet component library, please check the following resources:

- [Overview of vleaflet](docs/vue-docs-zh-cn/src/vleaflet/overview.md)
- [Quick Start Guide](docs/vue-docs-zh-cn/src/vleaflet/quick-start.md)

## Contributing

We welcome contributions to the vleaflet project! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Next Steps
Explore the Map Component Guide to dive deeper into vleaflet's features