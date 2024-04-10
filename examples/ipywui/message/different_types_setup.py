
def setup(props, ctx, vm):
    def show_success():
        vm.message.success({
            'message': 'Congrats, this is a success message.',
        })

    def show_info():
        vm.message.info({
            'message': 'This is message.',
        })

    def show_warning():
        vm.message.warning({
            'message': 'Warning, this is a warning message.',
        })

    def show_error():
        vm.message.error({
            'message': 'Oops, this is a error message.',
        })

    return locals()
