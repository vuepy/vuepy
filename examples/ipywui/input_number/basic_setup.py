from vuepy import ref


def setup(props, ctx, vm):
    num = ref(1)
    num_float = ref(1.1)
    return locals()
