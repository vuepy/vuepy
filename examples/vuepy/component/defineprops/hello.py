from vuepy import defineProps

def setup(props, ctx, app):
    props = defineProps(['name'])
    return locals()
