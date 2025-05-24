# coding: utf-8
# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------

class FactoryMeta(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._registry = {}

    def register(cls, name=None):
        def _(sub_cls):
            _name = name or (sub_cls.name() if callable(sub_cls.name) else sub_cls.name)
            cls._registry[_name] = sub_cls
            return sub_cls
        return _

    def get_all_registry(cls):
        return cls._registry

    def get_by_name(cls, name):
        return cls._registry.get(name, None)

    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)
