from vuepy import ref


def setup(props, ctx, vm):
    is_show = ref(True)

    def show_dialog():
        is_show.value = True

    def close_dialog():
        is_show.value = False

    return locals()
