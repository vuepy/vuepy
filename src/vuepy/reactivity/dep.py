from __future__ import annotations


class Dep(set):
    def __init__(self, *args, **kwargs):
        self.key = kwargs.pop('key', None)
        self.w = kwargs.pop('w', 0)  # wasTracked
        self.n = kwargs.pop('n', 0)  # newTracked
        super().__init__(*args, **kwargs)

    def add(self, effect) -> None:
        super().add(effect)

    def delete(self, effect) -> None:
        try:
            self.remove(effect)
        except Exception:
            pass


def createDep(effects=None, key=None) -> Dep:
    return Dep(effects or "", key=key)
