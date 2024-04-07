from vuepy import ref


def setup(props, ctx, vm):
    selection_options = [('0°C', 0), ('5°C', 5), ('10°C', 10), ('37°C', 37)]
    selection = ref(10)
    selection_range = ref([5, 37])

    return locals()
