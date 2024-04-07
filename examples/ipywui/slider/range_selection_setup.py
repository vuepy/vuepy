from vuepy import ref


def setup(props, ctx, vm):
    int_range = ref([1, 3])
    float_range = ref([1.1, 3.1])
    selection_range = ref(['a', 'c'])
    selection_options = ['a', 'b', 'c', 'd']

    return locals()
