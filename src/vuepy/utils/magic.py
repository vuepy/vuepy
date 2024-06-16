# coding: utf-8
import json
import logging
from pathlib import Path

from IPython.core.magic import register_line_magic

from ipywui import wui
from vuepy import log
from vuepy.compiler_sfc.compile import SFCFile
from vuepy.runtime.core.api_create_app import create_app
from vuepy.runtime.core.import_sfc import import_sfc


class LogLevelScope:
    def __init__(self, logger: logging.Logger, level=logging.ERROR):
        self.logger = logger
        self.org_level = logger.level
        self.level = level

    def __enter__(self):
        self.logger.setLevel(self.level)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.setLevel(self.org_level)


@register_line_magic
def vuepy_import(vue_sfc):
    """
    import vue sfc file

    ```python
    from vuepy import create_app
    from vuepy.utils import magic

    App=%vuepy_import test.vue
    app = create_app(App)
    app.mount()
    ```

    :param vue_sfc:
    :return: App
    """
    return import_sfc(vue_sfc)


@register_line_magic
def vuepy_demo(vue_sfc):
    """
    %vuepy_demo test.vue

    :param vue_sfc:
    :return:
    """
    sfc_file_path = Path(vue_sfc.strip())
    sfc_file = SFCFile.load(sfc_file_path)

    script_content = 0
    if sfc_file.script_src:
        _script_file = sfc_file.file.parent / sfc_file.script_src
        with open(_script_file) as f:
            _comment = f'# {sfc_file.script_src}\n\n'
            script_content = _comment + f.read()

    sfc_file_comment = f'<!-- {sfc_file_path} -->\n'
    print(json.dumps({
        'vue': sfc_file_comment + sfc_file.content,
        'setup': script_content,
    }))

    with LogLevelScope(log.getLogger()):
        App = import_sfc(sfc_file_path)
        app = create_app(App).use(wui)
        return app.mount()


@register_line_magic
def vuepy_log(cmd):
    """
    show log.

    :param cmd: clear
    :return:
    """
    if cmd == 'clear':
        log.logout.clear_output()
    return log.logout
