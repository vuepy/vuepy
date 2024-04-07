from vuepy import ref


def setup(props, ctx, vm):
    copytext = ref("hello")

    return locals()
