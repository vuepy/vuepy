import io
import numpy as np
from PIL import Image


def setup(props, ctx, vm):
    img_array = np.zeros([100, 100, 3], dtype=np.uint8)
    img_array[:, :, 2] = 200
    buf = io.BytesIO()

    img = Image.fromarray(img_array)
    # to rgb img
    img.save(buf, format="PNG")

    rgb_png = buf.getvalue()


    img_array = np.zeros([100, 100, 1], dtype=np.uint8)
    img_array += 122
    buf = io.BytesIO()

    img = Image.fromarray(img_array.squeeze(), 'L')
    # to gray img
    img.save(buf, format="PNG")

    gray_png = buf.getvalue()

    return locals()
