from vuepy import ref


def setup(props, ctx, vm):
    choice1 = ref('1')
    dropdown_items1 = ['1', '2', '3']

    choice2 = ref(1)
    dropdown_items2 = [('One', 1), ('Two', 2), ('Three', 3)]

    return locals()
