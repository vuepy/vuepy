from vuepy import ref


def setup(props, ctx, vm):
    datetime = ref(None)

    def on_change(event):
        print(event) # {'new': datetime.datetime(2025, 3, 22, 12, 0), 'old': None, 'owner': DateTimePicker(...)}

    return locals()
