from vuepy.reactivity import ReactiveEffect


class Dep(set):
    def __init__(self, *args, **kwargs):
        self.w = kwargs.pop('w', 0)
        self.n = kwargs.pop('n', 0)
        super().__init__(*args, **kwargs)


def createDep(effects: ReactiveEffect = None) -> Dep:
    return Dep(effects or "")
