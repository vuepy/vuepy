from vuepy import ref


def setup(props, ctx, vm):
    color1 = ref("#8f8fcc")
    color2 = ref("green")

    return locals()
