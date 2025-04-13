from vuepy import defineEmits

def setup(props, ctx, app):
    emit = defineEmits(['submit'])

    def submit(ev):
        print(ev) # Button(description='submit', ...)
        emit('submit', 1, 2, 3)

    return locals()
