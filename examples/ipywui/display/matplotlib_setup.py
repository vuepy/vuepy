import matplotlib.pyplot as plt
import numpy as np

from vuepy import ref


def plt_sin():
    x = np.arange(0, 5 * np.pi, 0.1)
    y = np.sin(x)

    plt.plot(x, y, color='green')
    plt.xlabel('x')
    plt.ylabel('sin(x)')
    plt.title('Sine Curve using Matplotlib')
    plt.grid(True)
    # plt.show()
    im = plt.gcf()
    plt.close()
    return im


def plt_cos():
    x = np.arange(0, 5 * np.pi, 0.1)
    y = np.cos(x)

    plt.plot(x, y, color='blue')
    plt.xlabel('x')
    plt.ylabel('cos(x)')
    plt.title('Cosine Curve using Matplotlib')
    plt.grid(True)
    # plt.show()
    im = plt.gcf()
    plt.close()
    return im


def plt_scatter():
    np.random.seed(1)
    data_x = np.random.randn(100)
    data_y = np.random.randn(100)

    plt.scatter(data_x, data_y, color='blue', alpha=0.5)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Scatter Plot Example')
    plt.grid(True)
    # plt.show()
    im = plt.gcf()
    plt.close()
    return im


def setup(props, ctx, vm):
    plt1 = ref(plt_sin())
    plt2 = ref(plt_scatter())
    plt3 = ref(plt_cos())

    return locals()
