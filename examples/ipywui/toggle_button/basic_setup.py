from vuepy import ref


def setup(props, ctx, vm):
    val1 = ref(True)
    return locals()
