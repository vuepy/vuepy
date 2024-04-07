from vuepy import ref


def setup(props, ctx, vm):
    choices = ref([])

    choices2 = ref(['Linux', 'macOS'])
    return locals()
