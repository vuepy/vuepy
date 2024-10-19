import io


def convert_pil_image_to_bin(img, format=None) -> bytes:
    """

    :param img: PIL.Image
    :param format: PNG
    :return:
    """
    with io.BytesIO() as buf:
        img.save(buf, format=format or img.format)
        return buf.getvalue()


def convert_opencv_image_to_bin(img, format='.png') -> bytes:
    """

    :param img: opencv img(ndarray)
    :param format: .png .jpg
    :return:
    """
    import cv2 as cv
    _, img_encoded = cv.imencode(format, img)
    with io.BytesIO(img_encoded.tobytes()) as buf:
        return buf.getvalue()
