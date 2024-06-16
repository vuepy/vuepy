from vuepy import ref


def setup(props, ctx, vm):
    is_show = ref(True)

    state = ref("-")

    def show():
        is_show.value = True

    def close():
        is_show.value = False

    def handle_open():
        state.value = 'open'

    def handle_close():
        state.value = 'close'

    return locals()
