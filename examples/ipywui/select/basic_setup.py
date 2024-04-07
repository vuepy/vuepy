from vuepy import ref


def setup(props, ctx, vm):
    choice = ref('macOS')

    choice2 = ref(1)
    radio_items = [('One', 1), ('Two', 2), ('Three', 3)]
    return locals()
