from vuepy.utils.factory import FactoryMeta


class VuepyAppStore(metaclass=FactoryMeta):
    @classmethod
    def register(cls, app_name, app=None):
        FactoryMeta.register(cls, app_name)(app)
        return app

    @classmethod
    def get(cls, app_name):
        return cls.get_all_registry().get(app_name)
