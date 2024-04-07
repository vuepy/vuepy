from vuepy import ref


def setup(props, ctx, vm):
    colors = ref(['red', 'green', '#0000ff'])
    return locals()
