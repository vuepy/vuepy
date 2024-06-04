# coding: utf-8
import json
from pathlib import Path

from IPython.core.magic import register_line_magic

from ipywui import wui
from vuepy import SFCFile
from vuepy import create_app
from vuepy import import_sfc
from vuepy import log


@register_line_magic
def vuepy_import(vue_sfc):
    """
    import vue sfc file

    ```python
    from ipywui import wui
    from vuepy import create_app
    from vuepy.utils import magic

    App=%vue_import test.vue
    app = create_app(App)
    app.use(wui)
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
        _script_file = sfc_file.file.parent.joinpath(sfc_file.script_src)
        with open(_script_file) as f:
            _script_content = f.read()

    print(json.dumps({
        'vue': sfc_file.content,
        'setup': script_content,
    }))

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
