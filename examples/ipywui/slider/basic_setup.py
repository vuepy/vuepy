from vuepy import ref


def setup(props, ctx, vm):
    default = ref(None)
    init_val = ref(5)
    float_val = ref(10.1)
    selection_val = ref('a')
    selection_options = ['a', 'b', 'c', 'd']

    return locals()
