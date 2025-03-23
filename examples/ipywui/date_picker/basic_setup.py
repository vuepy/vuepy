from vuepy import ref


def setup(props, ctx, vm):
    date = ref(None)

    def on_change(event):
        print(event) # {'new': datetime.date(2025, 3, 22), 'old': None, 'owner': DatePicker(...)}

    return locals()
