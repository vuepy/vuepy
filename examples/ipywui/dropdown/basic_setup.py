from vuepy import ref


def setup(props, ctx, vm):
    dropdown_items1 = ['A', 'B', 'C']
    choice1 = ref(dropdown_items1[0])

    # list of (name, val)
    dropdown_items2 = [('One', 1), ('Two', 2), ('Three', 3)]
    choice2 = ref(dropdown_items2[0][1])

    def on_change(event):
        print(event) # {'new': 'A', 'old': 'B', 'owner': Dropdown(...)}

    def on_change2(event):
        print(event) # {'new': 1, 'old': 2, 'owner': Dropdown(...)}

    return locals()
