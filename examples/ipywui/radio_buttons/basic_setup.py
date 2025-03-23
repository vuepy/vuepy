from vuepy import ref


def setup(props, ctx, vm):
    options1 = ['pepperoni', 'pineapple', 'anchovies']
    choice1 = ref(options1[0])

    options2 = [('One', 1), ('Two', 2), ('Three', 3)]
    choice2 = ref(options2[0][1])

    def on_change1(event):
        print(event) # {'new': 'pineapple', 'old': 'pepperoni', 'owner': RadioButtons(...)}

    def on_change2(event):
        print(event) # {'new': 2, 'old': 1, 'owner': RadioButtons(...)} 

    return locals()
