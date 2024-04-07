from vuepy import ref


def setup(props, ctx, vm):
    nums = ref([1, 2, 3])
    int_nums = ref([1, 2, 3])

    return locals()
