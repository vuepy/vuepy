from typing import List

from vuepy.reactivity import ReactiveEffect
from vuepy.reactivity import effect


class Dep(set):
    def __init__(self, *args, **kwargs):
        self.w = kwargs.pop('w', 0)
        self.n = kwargs.pop('n', 0)
        super().__init__(*args, **kwargs)


def createDep(effects: ReactiveEffect = None) -> Dep:
    return Dep(effects or "")


def wasTracked(dep: Dep):
    return (dep.w & effect.trackOpBit) > 0


def newTracked(dep: Dep):
    return (dep.n & effect.trackOpBit) > 0


def initDepMarkers(deps: List[Dep]):
    for dep in deps:
        dep.w |= effect.trackOpBit


def finalizeDepMarkers(effect):
    # todo 可优化
    ptr = 0
    for dep in effect.deps:
        if wasTracked(dep) and (not newTracked(dep)):
            continue
        else:
            dep.w &= ~effect.trackOpBit
            dep.n &= ~effect.trackOpBit
            effect.deps[ptr] = dep
            ptr += 1
    effect.deps = effect.deps[:ptr]

