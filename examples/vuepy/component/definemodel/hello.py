from vuepy import defineModel

def setup(props, ctx, app):
    model = defineModel() # default
    model.value = 'world'

    return locals()
