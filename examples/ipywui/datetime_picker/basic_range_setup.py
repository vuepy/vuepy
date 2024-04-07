import datetime

from vuepy import ref


def setup(props, ctx, vm):
    time = ref(None)

    tz = datetime.timezone(datetime.timedelta(seconds=28800), 'CST')
    min_time = datetime.datetime(2021, 1, 1, tzinfo=tz)
    max_time = datetime.datetime(2024, 1, 1, tzinfo=tz)

    return locals()
