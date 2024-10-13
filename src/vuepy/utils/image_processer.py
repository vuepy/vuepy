import io


def convert_pil_image_to_bin(img, format=None):
    """

    :param img: PIL.Image
    :param format: PNG
    :return:
    """
    with io.BytesIO() as buf:
        img.save(buf, format=format or img.format)
        return buf.getvalue()
