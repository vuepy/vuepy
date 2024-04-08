from vuepy import ref


def setup(props, ctx, vm):
    selected = ref('s1')

    def to(label):
        selected.value = label

    return locals()
