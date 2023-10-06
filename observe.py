#!coding: utf-8
from collections import defaultdict


class ReactiveField:
    def __init__(self, field_name, data):
        self.field_name = field_name
        self._data = data

    def __get__(self, instance, owner):
        return self._data[self.field_name]

    def __set__(self, instance: 'Vue', new_value):
        self._data[self.field_name] = new_value

        instance.render()
        # TODO
        # dep.notify()


class ReactiveDict(dict):
    target = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deps = defaultdict(Dep)

    def __getitem__(self, attr):
        # print(f'get attr {attr}')
        if self.target:
            self.deps[attr].add_sub(self.target)

        return super().__getitem__(attr)

    def __setitem__(self, attr, value):
        # print(f'set attr {attr}: {value}')
        super().__setitem__(attr, value)
        self.deps[attr].notify()

    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __setattr__(self, attr, value):
        self.__setitem__(attr, value)


def observe(data):
    def define_reactive(_data):
        for k, v in _data.items():
            _data[k] = observe(v)
        return _data

    if not isinstance(data, dict):
        return data

    define_reactive(data)
    return ReactiveDict(data)


class Dep:
    target = None

    def __init__(self):
        self.subs = []

    def add_sub(self, sub):
        if sub in self.subs:
            return

        self.subs.append(sub)

    def notify(self):
        for sub in self.subs:
            sub.update()


def get_attr_by_dot_chain(data, dot_chain):
    attrs = dot_chain.split('.')
    _data = data
    for attr in attrs:
        _data = getattr(_data, attr)
    return _data


def set_attr_by_dot_chain(data, dot_chain, val):
    attrs = dot_chain.rsplit('.', 1)
    if len(attrs) == 1:
        attr_set = attrs[0]
        _data = data
    else:
        _attr_get, attr_set = attrs
        _data = get_attr_by_dot_chain(data, _attr_get)

    setattr(_data, attr_set, val)


class Watcher:
    def __init__(self, vm: 'Vue', expr_or_fn, callback, options):
        self.vm = vm
        self.cb = callback
        self.exp = expr_or_fn
        self.options = options
        self.value = self.get()

    def get(self):
        Dep.target = self
        # value = getattr(self.vm, self.exp)
        value = get_attr_by_dot_chain(self.vm, self.exp)
        Dep.target = None
        return value

    def update(self):
        self.run()

    def run(self):
        value = self.get()
        old_val = self.value
        if value != old_val:
            self.value = value
            self.cb(self.vm, value, old_val)

    def add_dep(self):
        pass
