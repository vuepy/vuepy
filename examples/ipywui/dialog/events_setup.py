from vuepy import ref


def setup(props, ctx, vm):
    is_show = ref(False)

    state = ref("-")

    def show_dialog():
        is_show.value = True

    def close_dialog():
        is_show.value = False

    def handle_open():
        state.value = 'open'

    def handle_close():
        state.value = 'close'

    return locals()
