from vuepy import ref


def setup(props, ctx, vm):
    options1 = ['pepperoni', 'pineapple', 'anchovies']
    choice1 = ref('pepperoni')

    options2 = [('One', 1), ('Two', 2), ('Three', 3)]
    choice2 = ref(1)

    return locals()
