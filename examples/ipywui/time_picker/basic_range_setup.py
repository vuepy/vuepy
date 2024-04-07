import datetime

from vuepy import ref


def setup(props, ctx, vm):
    time = ref(None)
    min_time = datetime.time(10, 10, 0)
    max_time = datetime.time(12, 10, 0)

    return locals()
