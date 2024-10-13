import matplotlib.pyplot as plt
import numpy as np

from vuepy import ref


def plt_to_img(title, xlabel, ylabel):
    """
    plt to matplotlib.figure.Figure
    """
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    # plt.show()
    im = plt.gcf()
    plt.close()
    return im


def plt_sin():
    x = np.arange(0, 5 * np.pi, 0.1)
    y = np.sin(x)
    plt.plot(x, y, color='green')
    return plt_to_img('Sine Curve using Matplotlib', 'x', 'sin(x)')


def plt_cos():
    x = np.arange(0, 5 * np.pi, 0.1)
    y = np.cos(x)
    plt.plot(x, y, color='blue')
    return plt_to_img('Cosine Curve using Matplotlib', 'x', 'sin(x)')


def plt_scatter():
    np.random.seed(1)
    data_x = np.random.randn(100)
    data_y = np.random.randn(100)
    plt.scatter(data_x, data_y, color='blue', alpha=0.5)
    return plt_to_img('Scatter Plot Example', 'x', 'y')


def setup(props, ctx, vm):
    plt1 = ref(plt_sin())
    plt2 = ref(plt_scatter())
    plt3 = ref(plt_cos())

    return locals()
