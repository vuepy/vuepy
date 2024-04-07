from vuepy import ref


def setup(props, ctx, vm):
    checked1 = ref(True)
    checked2 = ref(True)
    checked3 = ref(True)

    return locals()
