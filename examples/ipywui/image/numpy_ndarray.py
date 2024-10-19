import numpy as np
from PIL import Image

from vuepy.utils.image_processer import convert_opencv_image_to_bin
from vuepy.utils.image_processer import convert_pil_image_to_bin


def setup(props, ctx, vm):
    img_array = np.zeros([100, 100, 3], dtype=np.uint8)
    img_array[:, :, 2] = 200
    # ndarray to rgb img
    rgb_png = Image.fromarray(img_array, mode='RGB')
    # 必须指定format
    rgb_png.format = 'PNG'


    img_array = np.zeros([100, 100, 1], dtype=np.uint8)
    img_array += 122
    # ndarray to gray img
    img = Image.fromarray(img_array.squeeze(), 'L')
    gray_png = convert_pil_image_to_bin(img, 'PNG')


    import cv2 as cv
    cv_img = cv.imread("jupyter_logo.png", cv.IMREAD_UNCHANGED)

    # method1: opencv to pil
    img_png = Image.fromarray(cv.cvtColor(cv_img, cv.COLOR_BGRA2RGBA))
    img_png.format = "PNG"

    # # method2: opencv to bin
    # img_png = convert_opencv_image_to_bin(cv_img, '.png')

    return locals()
