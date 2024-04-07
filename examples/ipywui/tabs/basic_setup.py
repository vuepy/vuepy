from vuepy import ref


def setup(props, ctx, vm):
    selected = ref(1)

    return locals()
