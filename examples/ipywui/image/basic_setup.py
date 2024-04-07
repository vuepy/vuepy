from vuepy import ref


def setup(props, ctx, vm):
    file = open("jupyter_logo.png", "rb")
    img = ref(file.read())

    return locals()
