
def setup(props, ctx, vm):
    def show_msg():
        vm.message.info({
            'message': 'This is message.',
            'duration': 2000,
        })

    return locals()
