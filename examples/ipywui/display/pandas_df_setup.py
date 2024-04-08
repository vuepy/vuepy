import pandas as pd

from vuepy import ref


def setup(props, ctx, vm):
    df1 = ref(pd.DataFrame(data={
        'col1': [1, 2],
        'col2': [3, 4],
        'col3': [5, 6],
    }))

    df2 = ref(pd.DataFrame(data={
        'col1': ['a', 'b'],
        'col2': ['c', 'd'],
        'col3': ['e', 'f'],
    }))

    return locals()
