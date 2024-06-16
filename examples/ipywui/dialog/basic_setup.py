from vuepy import ref


def setup(props, ctx, vm):
    is_show = ref(True)

    def show():
        is_show.value = True

    def close():
        is_show.value = False

    return locals()
