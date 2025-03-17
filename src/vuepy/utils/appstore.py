# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from typing import Type
from typing import Union

from vuepy.compiler_sfc.codegen import VueComponent
from vuepy.compiler_sfc.sfc_codegen import SFCType
from vuepy.utils.factory import FactoryMeta


class VuepyAppStore(metaclass=FactoryMeta):
    """
    VuepyAppStore stores all the Vuepy App: Union[Type[VueComponent], SFCType])).
    """

    @classmethod
    def register(cls, app_name, app: Union[Type[VueComponent], SFCType]):
        """
        Register a Vuepy Component.

        :param app_name: The name of the App.
        :param app: The App to register.
        :return:
        """
        FactoryMeta.register(cls, app_name)(app)
        return app

    @classmethod
    def get(cls, app_name) -> Union[Type[VueComponent], SFCType]:
        """
        Get a Vuepy App by name.

        :param app_name: The name of the App.
        :return: The App.
        """
        return cls.get_all_registry().get(app_name)
