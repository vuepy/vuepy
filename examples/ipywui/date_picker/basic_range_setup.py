import datetime

from vuepy import ref


def setup(props, ctx, vm):
    day = ref(None)

    min_day = datetime.date(2021, 1, 1)
    max_day = datetime.date(2024, 1, 1)

    return locals()
