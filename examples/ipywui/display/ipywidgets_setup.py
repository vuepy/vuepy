import ipywidgets as widgets
from IPython.display import display

from vuepy import ref


def setup(props, ctx, vm):
    a = widgets.IntSlider(description='a')
    b = widgets.IntSlider(description='b')
    c = widgets.IntSlider(description='c')

    def f(a, b, c):
        html = '<p style="color: red">{}*{}*{}={}</p>'.format(a, b, c, a * b * c)
        display(widgets.HTML(html))

    out = widgets.interactive_output(f, {'a': a, 'b': b, 'c': c})

    hbox = widgets.HBox([widgets.VBox([a, b, c]), out])

    widget = ref(hbox)

    return locals()
