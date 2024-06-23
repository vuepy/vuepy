<h1>
<p align="center">
  Vue.py
</h1>
<samp>
  <p align="center">
    <span>a progressive, incrementally-adoptable Python framework <br>for building UI on the IPython Notebook.</span>
      <br>
      <br>
      <a href="#installation">installation</a> .
      <a href="https://www.vuepy.org/guide/introduction.html">docs</a> .
      <!--<a href="">discord</a> .-->
      <a href="https://www.vuepy.org/guide/quick-start.html">learn</a>
  </p>
</samp>
</p>

## About

Vue.py (pronounced /vjuːpaɪ/, like "view py") is a Python framework for building user interfaces. It is built upon standard HTML, CSS, and Python, offering a declarative and component-based programming model that aids in the efficient development of user interfaces. Vue.py is capable of handling both simple and complex interfaces.

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


Read [the documentation](https://www.vuepy.org/guide/quick-start.html) to learn
more.

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

## License

[MIT](https://github.com/vuepy/vuepy/blob/master/LICENSE)