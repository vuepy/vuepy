
def setup(props, ctx, vm):
    def show_success():
        msg = vm.message.success({
            'message': 'Congrats, this is a success message.',
            'show_close': True,
        })
        # msg.close()

    def show_info():
        vm.message.info({
            'message': 'This is message.',
            'show_close': True,
        })

    def show_warning():
        vm.message.warning({
            'message': 'Warning, this is a warning message.',
            'show_close': True,
        })

    def show_error():
        vm.message.error({
            'message': 'Oops, this is a error message.',
            'show_close': True,
        })

    return locals()
