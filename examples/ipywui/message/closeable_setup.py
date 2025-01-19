
def setup(props, ctx, vm):
    def show():
        msg = vm.message.success({
            'message': 'Congrats, this is a success message.',
            'show_close': True,
        })
        # tips: you can use msg.close() to close the message box
        # msg.close()

    return locals()
