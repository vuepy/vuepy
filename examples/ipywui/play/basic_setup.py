from vuepy import ref


def setup(props, ctx, vm):
    frame = ref(1)
    frame2 = ref(1)
    return locals()
