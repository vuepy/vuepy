from vuepy import ref


def setup(props, ctx, vm):
    tags = ref(['tag1', 'tag2', 'tag3'])
    unique_tags = ref(['t1', 't2', 't3'])
    return locals()
